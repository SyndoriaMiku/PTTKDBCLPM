from datetime import datetime, timedelta
from django.db.models import Count

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Post, Like
from .serializers import UserSerializer, PostSerializer, PostDetailSerializer

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