from django.urls import path
from .views import VideoListCreate, VideoDetail

urlpatterns = [
    path("", VideoListCreate.as_view(), name="video-list-create"),
    path("<str:pk>/", VideoDetail.as_view(), name="video-detail"),
]
