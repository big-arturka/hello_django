from django import template

register = template.Library()


@register.filter
def liked_by(obj, user):
    return obj.liked_by(user)
