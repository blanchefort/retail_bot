"""Главная страница представления менеджера сервиса
"""
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseNotFound
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User

@login_required(login_url='/accounts/login/')
def index(request):
    """Точка входа менеджера сервиса
    """
    if request.user.profile.type != 5:
        raise PermissionDenied

    context = {
        # Заголовок текущей страницы
        'title': 'Менеджмент сервиса',
        # отображаемое на сайте имя пользователя
        'screenname': request.user.first_name or request.user.username
    }

    return TemplateResponse(request, 'manager/index.html', context=context)