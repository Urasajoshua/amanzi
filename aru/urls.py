from django.contrib import admin
from django.urls import path, include
from authentication.views import (
    UserListCreateAPIView, UserRetrieveUpdateDestroyAPIView,
    DissertationListCreateAPIView, DissertationRetrieveUpdateDestroyAPIView,
    CommentListCreateAPIView, CommentRetrieveUpdateDestroyAPIView,
    SupervisionListCreateAPIView, SupervisionRetrieveUpdateDestroyAPIView,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('api/users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),
    path('api/dissertations/', DissertationListCreateAPIView.as_view(), name='dissertation-list-create'),
    path('api/dissertations/<int:pk>/', DissertationRetrieveUpdateDestroyAPIView.as_view(), name='dissertation-detail'),
    path('api/comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('api/comments/<int:pk>/', CommentRetrieveUpdateDestroyAPIView.as_view(), name='comment-detail'),
    path('api/supervisions/', SupervisionListCreateAPIView.as_view(), name='supervision-list-create'),
    path('api/supervisions/<int:pk>/', SupervisionRetrieveUpdateDestroyAPIView.as_view(), name='supervision-detail'),
    path('auth/',include('authentication.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
