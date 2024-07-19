from django.urls import path
from .views import UserLoginAPIView,DepartmentListCreateView,CourseListCreateView,signup,login,SupervisorListView ,StudentsBySupervisorView,DashboardData,DissertationUploadView,StudentsByCourseView,DissertationStatusUpdateView,VerifiedDissertationListView,UnverifiedDissertationListView

urlpatterns = [
    
    path('api/login/', UserLoginAPIView.as_view(), name='login'),
    path('departments/', DepartmentListCreateView.as_view(), name='department-list-create'),
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('signup/', signup, name='signup'),
    path('login/',login,name='login'),
    path('supervisors/', SupervisorListView.as_view(), name='supervisor-list'),
    path('supervisor/<int:supervisor_id>/students/', StudentsBySupervisorView.as_view(), name='students-by-supervisor'),
    path('api/dashboard-data/', DashboardData.as_view(), name='dashboard-data'),
    path('api/dissertations/', DissertationUploadView.as_view(), name='dissertation-upload'),
    path('courses/<int:course_id>/students/', StudentsByCourseView.as_view(), name='students-by-course'),
    path('dissertations/<int:pk>/', DissertationStatusUpdateView.as_view(), name='update_dissertation_status'),
    path('verified/',VerifiedDissertationListView.as_view()),
    path('unverified/',UnverifiedDissertationListView.as_view())
    

   

    
]
