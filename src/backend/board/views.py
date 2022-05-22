from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import Post
from .serializers import PostSerializer
from .aws_link import insert_recruitment


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().select_related("author")
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # 전체 공개, 필요시 인증 적용

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

        return super().perform_create(serializer)
