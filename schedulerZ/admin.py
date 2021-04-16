from django.contrib import admin
from schedulerZ.models import Notes

from django.conf.locale.ru import formats as ru_formats
ru_formats.DATE_FORMAT = 'd.m.Y H:i:s'


@admin.register(Notes)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'public', 'date', 'id')
    fields = ('date', ('title', 'public'), 'message')
    readonly_fields = ('date', )
    search_fields = ['title', 'message', ]
    list_filter = ('public', 'important', 'status', )

    def save_model(self, request, obj, form, change):
        # Добавляем текущего пользователя (если не выбран) при сохранении модели
        # docs: https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.save_model
        if not hasattr(obj, 'author') or not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)
