from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Category, Topic, Post
from .serializers import CategorySerializer, TopicSerializer, PostSerializer
from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView
from .permissions import CustomDjangoModelPermissions


@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        qs = Category.objects.all()
        serializer = CategorySerializer(qs, many=True)
        return Response(serializer.data)

    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def category_detail(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(CategorySerializer(category).data)

    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def category_topics(request, pk):
    topics = Topic.objects.filter(category_id=pk)
    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data)



@api_view(['GET', 'POST'])
def topic_list(request):
    if request.method == 'GET':
        qs = Topic.objects.all()
        serializer = TopicSerializer(qs, many=True)
        return Response(serializer.data)

    serializer = TopicSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def topic_detail(request, pk):
    try:
        topic = Topic.objects.get(pk=pk)
    except Topic.DoesNotExist:
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(TopicSerializer(topic).data)

    elif request.method == 'PUT':
        serializer = TopicSerializer(topic, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        serializer = TopicSerializer(topic, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        topic.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def post_list(request):

    if request.method == 'GET':
        qs = Post.objects.all()
        serializer = PostSerializer(qs, many=True)
        return Response(serializer.data)

    if not request.user.is_authenticated:
        return Response({'detail': 'Authentication required'}, status=401)

    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def post_detail(request, pk):
    try:
        obj = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    return Response(PostSerializer(obj).data)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_update(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    if post.created_by != request.user:
        if not request.user.has_perm('posts.can_edit_others_posts'):
            return Response(
                {'error': 'Nie masz uprawnień do edycji cudzych postów.'},
                status=403
            )

    serializer = PostSerializer(post, data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=post.created_by)
        return Response(serializer.data)

    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_delete(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_posts(request):
    posts = Post.objects.filter(created_by=request.user)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def category_search(request, name):
    qs = Category.objects.filter(name__icontains=name)
    return Response(CategorySerializer(qs, many=True).data)


@api_view(['GET'])
def topic_search(request, name):
    qs = Topic.objects.filter(name__icontains=name)
    return Response(TopicSerializer(qs, many=True).data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def category_secure_detail(request, pk):
    if not request.user.has_perm('posts.view_category'):
        raise PermissionDenied("Nie masz uprawnienia do przeglądania kategorii.")

    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    return Response(CategorySerializer(category).data)


class CategoryPermissionView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CustomDjangoModelPermissions]

    def get_queryset(self):
        return Category.objects.all()

    def get_object(self, pk):
        return Category.objects.get(pk=pk)

    def get(self, request, pk):
        category = self.get_object(pk)
        return Response(CategorySerializer(category).data)

    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response(status=204)