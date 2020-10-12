from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible

from .models import STATUS_CHOICES, Article, Comment

default_status = STATUS_CHOICES[0][0]


BROWSER_DATETIME_FORMAT = '%d.%m.%Y %H:%M'


class XDatepickerWidget(forms.TextInput):
    template_name = 'widgets/xdatepicker_widget.html'


def at_least_10(string):
    if len(string) < 10:
        raise ValidationError('This value is too short!')


@deconstructible
class MinLengthValidator(BaseValidator):
    message = 'Value "%(value)s" has length of %(show_value)d! It should be at least %(limit_value)d symbols long!'
    code = 'too_short'

    def compare(self, value, limit):
        return value < limit

    def clean(self, value):
        return len(value)


class ArticleForm(forms.ModelForm):
    publish_at = forms.DateTimeField(required=False, label='Время публикации',
                                     input_formats=['%Y-%m-%d', BROWSER_DATETIME_FORMAT,
                                                    '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M',
                                                    '%Y-%m-%d %H:%M:%S'],
                                     widget=XDatepickerWidget)

    class Meta:
        model = Article
        fields = ['title', 'text', 'status', 'publish_at', 'tags']
        widgets = {'tags': forms.CheckboxSelectMultiple}

    def clean(self):
        cleaned_data = super().clean()
        errors = []
        text = cleaned_data.get('text')
        title = cleaned_data.get('title')
        if text and title and text == title:
            errors.append(ValidationError("Text of the article should not duplicate it's title!"))
        if errors:
            raise ValidationError(errors)
        return cleaned_data


# class CommentForm(forms.Form):
#     article = forms.ModelChoiceField(queryset=Article.objects.all(), required=True, label='Статья')


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Найти")


class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
