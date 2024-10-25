from rest_framework import generics, permissions
from .models import User, Dissertation, Comment, Supervision,Department,Course
from .serializers import UserSerializer, DissertationSerializer, CommentSerializer, SupervisionSerializer , UserLoginSerializer,DepartmentSerializer,CourseCreateSerializer,CourseSerializer,DissertationUploadSerializer,DissertationStatusUpdateSerializer,AssignStudentsToSupervisorSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from .serializers import PasswordUpdateSerializer
from rest_framework.permissions import IsAuthenticated 
from rest_framework.permissions import AllowAny

class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

   

class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class DissertationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Dissertation.objects.all()
    serializer_class = DissertationSerializer

class DissertationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dissertation.objects.all()
    serializer_class = DissertationSerializer

class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class SupervisionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Supervision.objects.all()
    serializer_class = SupervisionSerializer

class SupervisionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supervision.objects.all()
    serializer_class = SupervisionSerializer



class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    

class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CourseCreateSerializer
        return CourseSerializer


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def login(request):
    email_or_regno = request.data.get('email_or_regno')
    password = request.data.get('password')

    if not email_or_regno or not password:
        return Response({'detail': 'Email/RegNo and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        if '@' in email_or_regno:
            # If input contains '@', assume it's an email
            user = User.objects.get(email=email_or_regno)
        else:
            # Otherwise, assume it's a RegNo and fetch corresponding user
            user = User.objects.get(RegNo=email_or_regno)

        # Now authenticate with fetched email and provided password
        authenticated_user = authenticate(request, username=user.email, password=password)

        if authenticated_user is not None:
            refresh = RefreshToken.for_user(authenticated_user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'RegNo': user.RegNo,
                    'firstname': user.firstname,
                    'middlename': user.middlename,
                    'surname': user.surname,
                    'role': user.role,
                }
            })
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    except User.DoesNotExist:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.MultipleObjectsReturned:
        return Response({'detail': 'Multiple users found. Please contact support.'}, status=status.HTTP_400_BAD_REQUEST)



class SupervisorListView(generics.ListAPIView):
    serializer_class = UserSerializer
    

    def get_queryset(self):
        return User.objects.filter(role='SUPERVISOR')
    

class StudentsBySupervisorView(APIView):
    

    def get(self, request, supervisor_id):
        # Get the supervisor
        supervisor = User.objects.filter(id=supervisor_id, role='SUPERVISOR').first()
        if not supervisor:
            return Response({"error": "Supervisor not found"}, status=404)

        # Get students supervised by this supervisor
        students = supervisor.students.all()

        # Serialize the student data
        serializer = UserSerializer(students, many=True)
        return Response(serializer.data)
    

class DashboardData(APIView):
    def get(self, request):
        departments_count = Department.objects.count()
        courses_count = Course.objects.count()
        dissertations_count = Dissertation.objects.count()
        verified_dissertations_count = Dissertation.objects.filter(status='VERIFIED').count()
        unverified_dissertations_count = Dissertation.objects.filter(status='PENDING').count()

        data = {
            'departments': departments_count,
            'courses': courses_count,
            'dissertations': dissertations_count,
            'verifiedDissertations': verified_dissertations_count,
            'unverifiedDissertations': unverified_dissertations_count,
        }

        return Response(data, status=status.HTTP_200_OK)
    

class DissertationUploadView(APIView):
    

    def post(self, request):
        data = request.data.copy()
        data['student'] = request.user.id  # Ensure the student is the logged-in user
        serializer = DissertationUploadSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class StudentsByCourseView(APIView):
    def get(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        
        students = User.objects.filter(course=course, role='STUDENT').prefetch_related('dissertations')
        serializer = UserSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class DissertationStatusUpdateView(generics.UpdateAPIView):
    queryset = Dissertation.objects.all()
    serializer_class = DissertationSerializer

    def patch(self, request, *args, **kwargs):
        dissertation = self.get_object()

        # Check if the user is a supervisor (you might want to adjust this logic as per your roles)
        if request.user.role != 'SUPERVISOR':
            raise PermissionDenied("You do not have permission to perform this action.")

        serializer = self.get_serializer(dissertation, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
class SupervisionCreateView(generics.CreateAPIView):
    queryset = Supervision.objects.all()
    serializer_class = SupervisionSerializer


@api_view(['POST'])
def assign_students_to_supervisor(request):
    if request.method == 'POST':
        serializer = AssignStudentsToSupervisorSerializer(data=request.data)
        if serializer.is_valid():
            # Assuming your serializer.save() logic or data handling
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VerifiedDissertationListView(generics.ListAPIView):
    queryset = Dissertation.objects.filter(status='VERIFIED')
    serializer_class = DissertationSerializer

class UnverifiedDissertationListView(generics.ListAPIView):
    queryset = Dissertation.objects.filter(status='PENDING')
    serializer_class = DissertationSerializer


class PasswordUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = PasswordUpdateSerializer(data=request.data)
        if serializer.is_valid():
            # Update password for the authenticated user
            serializer.update(request.user, serializer.validated_data)
            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([AllowAny])  # Allow access without authentication
def update_password_by_email(request):
    email = request.data.get('email')
    new_password = request.data.get('new_password')

    if not email or not new_password:
        return Response({'detail': 'Email and new password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
        user.set_password(new_password)  # Set the new password
        user.save()  # Save the user instance
        return Response({'detail': 'Password updated successfully.'}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)