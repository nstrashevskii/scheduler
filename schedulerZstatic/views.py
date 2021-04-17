from django.shortcuts import render
from schedulerZ.models import Notes
from scheduler.settings_local import server_version


def home(request):
    """ Использование Django шаблонов.  Метод обрабатывает запрос `/` """

    # Объект который будет передан в шаблон
    context = {
        'message': 'Текущий пользователь',
        'left': server_version(),
    }

    # Рендеринг шаблона с последующим ответом клиенту
    return render(request, 'schedulerZstatic/index.html', context)
