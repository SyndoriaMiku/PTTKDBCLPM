from datetime import datetime, timedelta
from django.db.models import Count

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Post, Like
from .serializers import UserSerializer, PostSerializer, PostDetailSerializer, LikeSerializer

# Create your views here.

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "userMsg": "Đăng ký thành công"
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(
            {
                "userMsg": "Đăng ký không thành công",
                "devMsg": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        
class GetPostByFilterAPIView(APIView):
    def get(self, request):
        author_id = request.query_params.get('author_id')
        month = int(request.query_params.get('month'), 0) #Default 0 get all
        order = request.query_params.get('order', 'desc') #Default desc
        
        if not author_id:
            return Response(
                {
                    "userMsg": "Xảy ra lỗi",
                    "devMsg": "Author_ID is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
            
        queryset = Post.objects.filter(author_id=author_id)
        
        if month > 0:
            start_date = datetime.now() - timedelta(days=30*month)
            queryset = queryset.filter(created_at__gte=start_date)
            
        if order == 'asc':
            queryset = queryset.order_by('like_count')
        else:
            queryset = queryset.order_by('-like_count')
        
        
        #Return data
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetPostDetailAPIView(APIView):
    def get(self, request, id):
        try:
            post = Post.objects.annotate(like_count=Count('likes')).get(id=id)
            serializer = PostDetailSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response(
                {
                    "userMsg": "Bài viết không tồn tại",
                    "devMsg": "Post not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
            
class LikePostAPIView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        post_id = request.data.get('post_id')
        status_like = request.data.get('status')
        
        #Validate Input
        if user_id is None or post_id is None or status_like is None:
            return Response(
                {
                    "userMsg": "Xảy ra lỗi",
                    "devMsg": "User_ID, Post_ID, Status are required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            user = User.objects.get(id=user_id)
            post = Post.objects.get(id=post_id)
            
            like, created = Like.objects.get_or_create(user=user, post=post)
            like.status = status_like
            like.save()
            
            return Response(
                {
                    "userMsg": "Thành công",
                    "devMsg": None
                },
                status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED
            )
            
        except User.DoesNotExist:
            return Response(
                {
                    "userMsg": "User không tồn tại",
                    "devMsg": "User not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Post.DoesNotExist:
            return Response(
                {
                    "userMsg": "Bài viết không tồn tại",
                    "devMsg": "Post not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )            
            