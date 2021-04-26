from django.db.models import Q
from rest_framework.decorators import api_view, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics, mixins, viewsets
from .models import Post, Comment, Category, PostImage, Like
from .serializers import CommentSerializer, CategorySerializer, PostImageSerializer, PostSerializer, LikeSerializer
from .permisions import IsAuthor


class MyPaginationClass(PageNumberPagination):
    page_size = 1

    def get_paginated_response(self, data):
        for i in range(self.page_size):
            text = data[i]['description']
            data[i]['description'] = text[:15] + '...'
            likes = data[i]['likes']
            data[i]['likes'] = len(likes)
            comments = data[i]['comments']
            data[i]['comments'] = len(comments)
        return super().get_paginated_response(data)

class PermMixin:
    def get_perm(self):
        if self.action == 'create':
            perm = [IsAuthenticated, ]
        elif self.action in ['update', 'partial_update', 'destroy']:
            perm = [IsAuthor, IsAuthenticated]
        else:
            perm = []
        return [i() for i in perm]

class PermForComment:
    def get_perm(self):
        if self.action == 'create':
            perm = [IsAuthenticated, ]
        elif self.action in ('update', 'partial_update', 'destroy'):
            perm = [IsAuthor, ]
        else:
            perm = []
        return [i() for i in perm]

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny, ]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]

    def get_permissions(self):
        """Переопределим данный метод"""
        print(self.action)
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthor, ]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions]


    @action(detail=False, methods=['get'])  # router builds path posts/search/?q=paris
    def search(self, request, pk=None):
        # print(request.query_params)
        q = request.query_params.get('q')           # request.query_params = request.GET
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) |
                                   Q(text__icontains=q))
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def sort(self, request):
        filter_ = request.query_params.get('filter')
        if filter_ == 'A-Z':
            queryset = self.get_queryset().order_by('title')
        elif filter_ == 'Z-A':
            queryset = self.get_queryset().order_by('-title')
        else:
            queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PostImageView(generics.ListCreateAPIView):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer

    def get_serializer_context(self):
        return {'request': self.request}

class CommentViewSet(PermMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class LikeViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated, ]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}