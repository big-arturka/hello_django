from django.urls import path

from api_v1.views import get_token_view, ArticleListView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView, \
    ArticleCreateView

app_name = 'api_v1'

urlpatterns = [
    path('get-token/', get_token_view, name='get_token'),
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('article/create/', ArticleDeleteView.as_view(), name='article_detail'),
    path('article/create/', ArticleCreateView.as_view(), name='article_create'),
    path('article/create/', ArticleUpdateView.as_view(), name='article_update'),
    path('article/create/', ArticleDeleteView.as_view(), name='article_delete'),
]