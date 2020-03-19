"""Менеджмент сообщений
"""
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseNotFound
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.conf import settings

from telegram_bot.models import Messages

@login_required(login_url='/accounts/login/')
def index(request):
    """Точка входа менеджера сервиса
    """
    if request.user.profile.type != 5:
        raise PermissionDenied

    context = {
        # Заголовок текущей страницы
        'title': 'Рассылка телеграм-пользователям',
        # отображаемое на сайте имя пользователя
        'screenname': request.user.first_name or request.user.username
    }

    if request.POST:
        message = request.POST.get('message').strip()
        if len(message) > 3:
            for user in User.objects.all():
                if user.profile.telegram_id:
                    Messages(
                        user=user,
                        chat_id=user.profile.telegram_id,
                        message=message,
                        actor=request.user,
                        reseived_flag=0
                    ).save()
                    messages.info(request, 'Сообщения поставлены в очередь на отправку.')
        else:
            messages.error(request, 'Сообщение не отправлено: кажется, вы ничего не написали.')

    context.update({'send_time': settings.TELEGRAM_SCHEDULE_TIME})

    return TemplateResponse(request, 'manager/messages.html', context=context)