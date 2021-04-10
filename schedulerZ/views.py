import math

from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime
from rest_framework.exceptions import APIException

from .models import Notes
from .serializers import NoteSerializer, NoteDetailSerializer, NoteEditorSerializer


def paginator_(notes, page_size, page_number):
    paginator = Paginator(notes, page_size)
    page_count = math.ceil(Notes.objects.count() / page_size)

    if page_count // page_number == 0:
        raise NotFound(f'Нет страницы с номером {page_number}')

    serializer = NoteSerializer(paginator.page(page_number), many=True)

    return serializer.data


def valid_date_data(request, new_note, status_):
    if 'date' in request.data:
        user_date = datetime.strptime(request.data['date'], "%Y-%m-%dT%I:%M:%S.%fZ")
        if user_date >= datetime.now():
            if new_note.is_valid():
                new_note.save(author=request.user)
                return Response(new_note.data, status=status.HTTP_201_CREATED)
            else:
                return Response(new_note.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            if new_note.is_valid():
                raise APIException(f'Введенная дата меньше текущей, формат даты "%Y-%m-%dT%I:%M:%S.%fZ"')
            else:
                raise APIException(f'Введенная дата меньше текущей, формат даты "%Y-%m-%dT%I:%M:%S.%fZ"')
    else:
        if new_note.is_valid():
            new_note.save(author=request.user)
            return Response(new_note.data, status=status_)
        else:
            return Response(new_note.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteView(APIView):
    """ все заметки, которые опубликованы """

    def get(self, request, page_number=1):
        """ Получить книги для блога """
        page_size = self.request.query_params.get('page_size', 5)
        notes = Notes.objects.filter(public=True).order_by('-date', 'title').select_related('author')
        return Response(paginator_(notes, page_size, page_number))


class NoteViewAuthor(APIView):
    """ все заметки одного автора """

    def get(self, request, page_number=1):
        """ Получить книги для блога """
        page_size = self.request.query_params.get('page_size', 5)
        notes = Notes.objects.filter(public=True, author=request.user).order_by('-date', 'title').select_related('author')
        return Response(paginator_(notes, page_size, page_number))


class NoteDetailView(APIView):

    def get(self, request, note_id):
        note = Notes.objects.select_related(
            'author'
        ).filter(
            pk=note_id, public=True
        ).first()

        if not note:
            raise NotFound(f'Опубликованная книга с id={note_id} не найдена')

        serializer = NoteDetailSerializer(note)
        return Response(serializer.data)


class NoteEditorView(APIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request):
        """ Новая заметка """
        new_note = NoteEditorSerializer(data=request.data)
        if 'date' in request.data:
            user_date = datetime.strptime(request.data['date'], "%Y-%m-%dT%I:%M:%S.%fZ")
            if user_date >= datetime.now():
                if new_note.is_valid():
                    new_note.save(author=request.user)
                    return Response(new_note.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(new_note.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                if new_note.is_valid():
                    raise APIException(f'Введенная дата меньше текущей, формат даты "%Y-%m-%dT%I:%M:%S.%fZ"')
                else:
                    raise APIException(f'Введенная дата меньше текущей, формат даты "%Y-%m-%dT%I:%M:%S.%fZ"')
        else:
            if new_note.is_valid():
                new_note.save(author=request.user)
                return Response(new_note.data, status=status.HTTP_201_CREATED)
            else:
                return Response(new_note.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, note_id):

        note = Notes.objects.filter(pk=note_id, author=request.user).first()
        if not note:
            raise NotFound(f'Заметка с id={note_id} для пользователя {request.user.username} не найдена')

        new_note = NoteEditorSerializer(note, data=request.data, partial=True)
        if 'date' in request.data:
            user_date = datetime.strptime(request.data['date'], "%Y-%m-%dT%I:%M:%S.%fZ")
            if user_date >= datetime.now():
                if new_note.is_valid():
                    new_note.save(author=request.user)
                    return Response(new_note.data, status=status.HTTP_200_OK)
                else:
                    return Response(new_note.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                if new_note.is_valid():
                    raise APIException(f'Введенная дата меньше текущей, формат даты "%Y-%m-%dT%I:%M:%S.%fZ"')
                else:
                    raise APIException(f'Введенная дата меньше текущей, формат даты "%Y-%m-%dT%I:%M:%S.%fZ"')

    def delete(self, request, note_id):
        note = Notes.objects.filter(pk=note_id, author=request.user)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
