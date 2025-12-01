from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Topic, Post
from .serializers import CategorySerializer, TopicSerializer, PostSerializer


@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        qs = Category.objects.all()
        return Response(CategorySerializer(qs, many=True).data)

    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    try:
        obj = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(CategorySerializer(obj).data)

    if request.method == 'PUT':
        serializer = CategorySerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def category_search(request, name):
    qs = Category.objects.filter(name__icontains=name)
    return Response(CategorySerializer(qs, many=True).data)

@api_view(['GET', 'POST'])
def topic_list(request):
    if request.method == 'GET':
        qs = Topic.objects.all()
        return Response(TopicSerializer(qs, many=True).data)

    serializer = TopicSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def topic_detail(request, pk):
    try:
        obj = Topic.objects.get(pk=pk)
    except Topic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(TopicSerializer(obj).data)

    if request.method == 'PUT':
        serializer = TopicSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def topic_search(request, name):
    qs = Topic.objects.filter(name__icontains=name)
    return Response(TopicSerializer(qs, many=True).data)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def post_list(request):

    if request.method == 'GET':
        qs = Post.objects.all()
        return Response(PostSerializer(qs, many=True).data)

    if not request.user.is_authenticated:
        return Response({"detail": "Authentication required"}, status=401)

    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, pk):
    try:
        obj = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(PostSerializer(obj).data)

    if request.method == 'PUT':
        serializer = PostSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=obj.created_by)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_posts(request):
    qs = Post.objects.filter(created_by=request.user)
    return Response(PostSerializer(qs, many=True).data)
