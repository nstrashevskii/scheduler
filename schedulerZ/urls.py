from django.urls import path
from . import views


app_name = 'schedulerZ'
urlpatterns = [
    path('notes/my/<int:page_number>', views.NoteViewAuthor.as_view(), name='notes'),
    path('notes/my/', views.NoteViewAuthor.as_view(), name='notes'),
    path('notes/<int:page_number>', views.NoteView.as_view(), name='notes'),
    path('notes/', views.NoteView.as_view(), name='notes'),
    path('note/<int:note_id>/', views.NoteDetailView.as_view(), name='note'),
    path('note/add/', views.NoteEditorView.as_view(), name='add'),
    path('note/edit/<int:note_id>/', views.NoteEditorView.as_view(), name='edit'),
    path('note/<int:note_id>/del/', views.NoteEditorView.as_view(), name='note_del'),
]