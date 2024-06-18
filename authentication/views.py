from rest_framework import generics, permissions
from .models import User, Dissertation, Comment, Supervision,Department,Course
from .serializers import UserSerializer, DissertationSerializer, CommentSerializer, SupervisionSerializer , UserLoginSerializer,DepartmentSerializer,CourseCreateSerializer,CourseSerializer,DissertationUploadSerializer,DissertationStatusUpdateSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework.views import APIView

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
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'firstname': user.firstname,
                'middlename': user.middlename,
                'surname': user.surname,
                'role': user.role,
            }
        })
    return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


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
    serializer_class = DissertationStatusUpdateSerializer


    def patch(self, request, *args, **kwargs):
        dissertation = self.get_object()

        # Check if the user is a supervisor
        if request.user.role != 'SUPERVISOR':
            return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        return self.partial_update(request, *args, **kwargs)