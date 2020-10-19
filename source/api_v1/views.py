import json

from django.http import HttpResponseNotAllowed, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.response import Response
from rest_framework.views import APIView

from api_v1.serializers import ArticleSerializer
from webapp.models import Article


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')


class ArticleListView(APIView):
    def get(self, request, *args, **kwargs):
        objects = Article.objects.all()
        slr = ArticleSerializer(objects, many=True)
        return Response(slr.data)


class ArticleDetailView(APIView):
    def get(self, request, *args, **kwargs):
        object = Article.objects.filter(pk=kwargs.get('pk'))
        slr = ArticleSerializer(object, many=True)
        return Response(slr.data)


class ArticleCreateView(APIView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        slr = ArticleSerializer(data=data)
        if slr.is_valid():
            article = slr.save()
            return Response(slr.data)
        else:
            response = Response(slr.errors)
            response.status_code = 400
            return response


class ArticleUpdateView(APIView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        instance = Article.objects.get(pk=kwargs.get('pk'))
        slr = ArticleSerializer(data=data, instance=instance)
        if slr.is_valid():
            article = slr.save()
            return Response(slr.data)
        else:
            response = Response(slr.errors)
            response.status_code = 400
            return response
        

class ArticleDeleteView(APIView):
    def post(self, request, *args, **kwargs):
        object = Article.objects.get(pk=kwargs.get('pk'))
        object.delete()
        return Response({'id': kwargs.get('pk')})
