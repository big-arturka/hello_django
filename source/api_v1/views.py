import json

from django.contrib.auth import get_user_model
from django.http import HttpResponseNotAllowed, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet

from api_v1.serializers import ArticleSerializer, UserSerializer
from webapp.models import Article


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')


class ArticleViewSet(ViewSet):
    queryset = Article.objects.all()

    def list(self, request):
        objects = Article.objects.all()
        slr = ArticleSerializer(objects, many=True)
        return Response(slr.data)

    def create(self, request):
        slr = ArticleSerializer(data=request.body)
        if slr.is_valid():
            article = slr.save()
            return Response(slr.data)
        else:
            return Response(slr.errors, status=400)

    def retrieve(self, request, pk=None):
        object = get_object_or_404(Article, pk=pk)
        slr = ArticleSerializer(object)
        return Response(slr.data)

    def update(self, request, pk=None):
        article = get_object_or_404(Article, pk=pk)
        slr = ArticleSerializer(data=request.data, instance=article)
        if slr.is_valid():
            article = slr.save()
            return Response(slr.data)
        else:
            return Response(slr.errors, status=400)

    def destroy(self, request, pk=None):
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return Response({'id': pk})


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
