from django.urls import path, include
from webapp.views import IndexView, ArticleCreateView, ArticleView, \
    ArticleUpdateView, ArticleDeleteView, \
    ArticleCommentCreateView, ArticleMassActionView, \
    CommentUpdateView, CommentDeleteView, ArticleLikeView, ArticleUnLikeView

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('article/', include([
        path('<int:pk>/', include([
            path('', ArticleView.as_view(), name='article_view'),
            path('update/', ArticleUpdateView.as_view(), name='article_update'),
            path('delete/', ArticleDeleteView.as_view(), name='article_delete'),
            path('comments/add/', ArticleCommentCreateView.as_view(),
                 name='article_comment_add'),
            path('like/', ArticleLikeView.as_view(), name='article_like'),
            path('unlike/', ArticleUnLikeView.as_view(), name='article_unlike'),
        ])),

        path('add/', ArticleCreateView.as_view(), name='article_create'),
        path('mass-action/', ArticleMassActionView.as_view(), name='article_mass_action'),
    ])),

    path('comment/', include([
        path('<int:pk>/', include([
            path('update/', CommentUpdateView.as_view(), name='comment_update'),
            path('delete/', CommentDeleteView.as_view(), name='comment_delete'),
        ]))
    ]))
]
