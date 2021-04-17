from rest_framework import serializers
from .models import Notes
from django.contrib.auth.models import User
from django.utils import timezone


class NoteSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Notes
        fields = ['id', 'title', 'message', 'public', 'author', 'important', 'date', ]


class AuthorSerializer(serializers.ModelSerializer):
    """ Автор статьи """

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined')


class NoteDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Notes
        exclude = ('public',)


class NoteEditorSerializer(serializers.ModelSerializer):
    """ Добавление или изменение статьи """
    author = AuthorSerializer(read_only=True)

    def validate_date(self, value):
        """
                Check that the blog post is about Django.
                """
        if value < timezone.now():
            raise serializers.ValidationError(f'Введенная дата меньше текущей, формат даты "%Y-%m-%dT%I:%M:%S.%fZ"')
        return value

    class Meta:
        model = Notes
        fields = "__all__"
        read_only_fields = ['author', ]
