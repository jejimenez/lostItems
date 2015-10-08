from django.shortcuts import render

# Create your views here.
from rest_framework import permissions, viewsets
from rest_framework.response import Response

from posts.models import Post
from posts.permissions import IsAuthorOfPost
from posts.serializers import PostSerializer
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.order_by('-created_at')
    serializer_class = PostSerializer
    parser_classes = (FileUploadParser, )#MultiPartParser, FormParser,)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), IsAuthorOfPost(),)

    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user, datafile =self.request.data.get('file'))
        return super(PostViewSet, self).perform_create(serializer)

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        print(serializer.data)
        return Response(serializer.data)



class AccountPostsViewSet(viewsets.ViewSet):
    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializer

    def list(self, request, account_username=None):
        queryset = self.queryset.filter(author__username=account_username)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)