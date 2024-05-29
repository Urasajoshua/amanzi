from rest_framework import generics, permissions
from .models import User, Dissertation, Comment, Supervision,Department,Course
from .serializers import UserSerializer, DissertationSerializer, CommentSerializer, SupervisionSerializer , UserLoginSerializer,DepartmentSerializer,CourseCreateSerializer,CourseSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate

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
