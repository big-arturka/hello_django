from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, \
    UserPassesTestMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.timezone import make_naive
from django.views.generic import View, DetailView, CreateView, UpdateView, DeleteView

from webapp.models import Article, Tag, ArticleLike
from webapp.forms import ArticleForm, BROWSER_DATETIME_FORMAT
from .base_views import SearchView


class IndexView(SearchView):
    template_name = 'article/index.html'
    context_object_name = 'articles'
    paginate_by = 2
    paginate_orphans = 0
    model = Article
    ordering = ['-created_at']
    search_fields = ['title__icontains', 'author__icontains']

    def get_queryset(self):
        data = super().get_queryset()
        if not self.request.GET.get('is_admin', None):
            data = data.filter(status='moderated')
        return data


class ArticleMassActionView(PermissionRequiredMixin, View):
    redirect_url = 'webapp:index'
    permission_required = 'webapp.delete_article'
    queryset = None  # изначально queryset = None

    def has_permission(self):
        if super().has_permission():
            return True  # админы и модеры могут удалять
        articles = self.get_queryset()
        author_ids = articles.values('author_id')
        for item in author_ids:
            if item['author_id'] != self.request.user.pk:
                return False  # остальные могут удалять, только если среди выбранных статей
        return True           # нет чужих статей

    # метод 'post' проверяет наличие ключа 'delete' в запросе,
    # и тогда удаляет
    def post(self, request, *args, **kwargs):
        if 'delete' in self.request.POST:
            return self.delete(request, *args, **kwargs)
        return redirect(self.redirect_url)

    # метод 'delete' не проверяет наличие ключа 'delete' в запросе,
    # и все равно удаляет
    def delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset.delete()
        return redirect(self.redirect_url)

    # "кэширующий" метод.
    # при первом доступе к свойству queryset находит и сохраняет его в self.queryset
    # при повторном доступе не ищет, возвращает сохранённое значение.
    def get_queryset(self):
        if self.queryset is None:
            ids = self.request.POST.getlist('selected_articles', [])
            self.queryset = self.get_queryset().filter(id__in=ids)
        return self.queryset


class ArticleView(DetailView):
    template_name = 'article/article_view.html'
    model = Article
    paginate_comments_by = 2
    paginate_comments_orphans = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        comments, page, is_paginated = self.paginate_comments(self.object)
        context['comments'] = comments
        context['page_obj'] = page
        context['is_paginated'] = is_paginated

        return context

    def paginate_comments(self, article):
        comments = article.comments.all().order_by('-created_at')
        if comments.count() > 0:
            paginator = Paginator(comments, self.paginate_comments_by, orphans=self.paginate_comments_orphans)
            page_number = self.request.GET.get('page', 1)
            page = paginator.get_page(page_number)
            is_paginated = paginator.num_pages > 1  # page.has_other_pages()
            return page.object_list, page, is_paginated
        else:
            return comments, None, False


class ArticleCreateView(LoginRequiredMixin, CreateView):
    template_name = 'article/article_create.html'
    form_class = ArticleForm
    model = Article

    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     response = super().form_valid(form)
    #     tag, _ = Tag.objects.get_or_create(name=self.request.user.username)
    #     form.instance.tags.add(tag)
    #     return response
    #
    # def get_success_url(self):
    #     return reverse('webapp:article_view', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        article.save()
        form.save_m2m()
        tag, _ = Tag.objects.get_or_create(name=self.request.user.username)
        article.tags.add(tag)
        return redirect('webapp:article_view', pk=article.pk)


class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'article/article_update.html'
    form_class = ArticleForm
    model = Article
    permission_required = 'webapp.change_article'

    def has_permission(self):
        article = self.get_object()
        return super().has_permission() or article.author == self.request.user

    def get_initial(self):
        return {'publish_at': make_naive(self.object.publish_at)\
            .strftime(BROWSER_DATETIME_FORMAT)}

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     tag, _ = Tag.objects.get_or_create(name=self.request.user.username)
    #     form.instance.tags.add(tag)
    #     return response
    #
    # def get_success_url(self):
    #     return reverse('webapp:article_view', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        article = form.save()
        tag, _ = Tag.objects.get_or_create(name=self.request.user.username)
        article.tags.add(tag)
        return redirect('webapp:article_view', pk=article.pk)


class ArticleDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'article/article_delete.html'
    model = Article
    success_url = reverse_lazy('webapp:index')

    def test_func(self):
        return self.request.user.has_perm('webapp.delete_article') or \
            self.get_object().author == self.request.user


class ArticleLikeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs.get('pk'))
        like, created = ArticleLike.objects.get_or_create(article=article, user=request.user)
        if created:
            article.like_count += 1
            article.save()
            return HttpResponse(article.like_count)
        else:
            return HttpResponseForbidden()


class ArticleUnLikeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs.get('pk'))
        like = get_object_or_404(article.likes, user=request.user)
        like.delete()
        article.like_count -= 1
        article.save()
        return HttpResponse(article.like_count)
