from django.shortcuts import render

from .models import Blog
from .serializers import BlogSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
'''
전체 블로그를 조회
'''
class BlogList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
	
    def post(self, request):
        serializer = BlogSerializer(data=request.data) # 요청 데이터(request.data)를 가지고 역직렬화를 수행해줄 수 있다.
        if serializer.is_valid(raise_exception = True): # 유효성 검사
            serializer.save(user=request.user) # 역직렬화해서 만들어낸 Blog 모델을 저장한다.
            return Response(serializer.data, status = status.HTTP_201_CREATED)
          
        return Response(status=status.HTTP_400_BAD_REQUEST)
'''
한 블로그 조회
'''

from .permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404

# @api_view(['GET', 'PUT', 'DELETE'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsOwnerOrReadOnly])

class BlogDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]
    def get_object(self, pk):
        blog = get_object_or_404(Blog, pk = pk)
        return blog
    
    def get(self, request, pk):
        blog = self.get_object(pk)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)
    
    def put(self, request, pk):
        blog = self.get_object(pk)
        serializer = BlogSerializer(blog, data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        blog = self.get_object(pk)
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)