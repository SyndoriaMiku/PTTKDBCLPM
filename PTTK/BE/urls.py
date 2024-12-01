from django.urls import path
import BE.views

urlpatterns = [
    path('register/', BE.views.RegisterAPIView.as_view(), name='register'),
    path('post/', BE.views.GetPostByFilterAPIView.as_view(), name='post'),
    path('post/<int:id>/', BE.views.GetPostDetailAPIView.as_view(), name='post_detail'),
    path('like/', BE.views.LikeAPIView.as_view(), name='like-post'),
]