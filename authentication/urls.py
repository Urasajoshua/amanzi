from django.urls import path
from .views import UserLoginAPIView,DepartmentListCreateView,CourseListCreateView,signup,login,SupervisorListView ,StudentsBySupervisorView

urlpatterns = [
    
    path('api/login/', UserLoginAPIView.as_view(), name='login'),
    path('departments/', DepartmentListCreateView.as_view(), name='department-list-create'),
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('signup/', signup, name='signup'),
    path('login/',login,name='login'),
    path('supervisors/', SupervisorListView.as_view(), name='supervisor-list'),
    path('supervisor/<int:supervisor_id>/students/', StudentsBySupervisorView.as_view(), name='students-by-supervisor'),

    
]
