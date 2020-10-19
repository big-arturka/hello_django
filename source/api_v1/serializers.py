from django.contrib.auth import get_user_model
from rest_framework import serializers
from webapp.models import Article, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(read_only=True, view_name='api_v1:user-detail')

    class Meta:
        model = get_user_model()
        fields = ['id','url', 'username', 'first_name', 'last_name', 'email']


class ArticleSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(read_only=True,
                                               view_name='api_v1:article-detail')
    author_url = serializers.HyperlinkedRelatedField(read_only=True, source='author',
                                                     view_name='api_v1:user-detail')
    author = UserSerializer(read_only=True)
    tags_display = TagSerializer(many=True, read_only=True, source='tags')

    class Meta:
        model = Article
        fields = ['id', 'url', 'title', 'text', 'author', 'author_url', 'status',
                  'created_at', 'updated_at', 'tags', 'tags_display']
        read_only_fields = ('author',)