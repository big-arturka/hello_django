from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from webapp.models import Comment, Article
from webapp.forms import ArticleCommentForm


class ArticleCommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'comment/comment_create.html'
    form_class = ArticleCommentForm

    def form_valid(self, form):
        article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        comment = form.save(commit=False)
        comment.article = article
        comment.author = self.request.user
        comment.save()
        # form.save_m2m()  ## для сохранения связей многие-ко-многим
        return redirect('webapp:article_view', pk=article.pk)


class CommentUpdateView(PermissionRequiredMixin, UpdateView):
    model = Comment
    template_name = 'comment/comment_update.html'
    form_class = ArticleCommentForm
    permission_required = 'webapp.change_comment'

    def has_permission(self):
        comment = self.get_object()
        return super().has_permission() or comment.author == self.request.user

    def get_success_url(self):
        return reverse('webapp:article_view', kwargs={'pk': self.object.article.pk})


class CommentDeleteView(PermissionRequiredMixin, DeleteView):
    model = Comment
    permission_required = 'webapp.delete_comment'

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def has_permission(self):
        comment = self.get_object()
        return super().has_permission() or comment.author == self.request.user

    def get_success_url(self):
        return reverse('webapp:article_view', kwargs={'pk': self.object.article.pk})
