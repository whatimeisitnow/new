from django.shortcuts import render

from .models import Blog
from .serializers import BlogSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

'''
전체 블로그를 조회
'''
@api_view(['GET', 'POST'])
def blog_list(request):
	if request.method == 'GET':
		blogs = Blog.objects.all()
		serializer = BlogSerializer(blogs, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)
	elif request.method == 'POST':
		serializer = BlogSerializer(data=request.data) # 요청 데이터(request.data)를 가지고 역직렬화를 수행해줄 수 있다.
		if serializer.is_valid(): # 유효성 검사
			serializer.save() # 역직렬화해서 만들어낸 Blog 모델을 저장한다.
			return Response(serializer.data, status = status.HTTP_201_CREATED)
	return Response(status=status.HTTP_400_BAD_REQUEST)
'''
한 블로그 조회
'''
@api_view(['GET', 'PUT', 'DELETE'])
def blog_detail(request, pk):
    try:
        blog = Blog.objects.get(pk=pk)
        if request.method == 'GET':
            serializer = BlogSerializer(blog)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            serializer = BlogSerializer(blog, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            blog.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)