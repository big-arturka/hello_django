from django.urls import path

from api_v1.views import get_token_view, ArticleListView

app_name = 'api_v1'

urlpatterns = [
    path('get-token/', get_token_view, name='get_token'),
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('article/create/', ArticleListView.as_view(), name='article_list')
]