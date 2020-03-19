"""Менеджмент продавцов
"""
from datetime import timedelta, datetime
import pytz

from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseNotFound
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User

from webpanel.models.profile import Profile
from webpanel.models.system_bill import SystemBill


@login_required(login_url='/accounts/login/')
def index(request):
    """Точка входа менеджера сервиса
    """
    if request.user.profile.type != 5:
        raise PermissionDenied

    context = {
        # Заголовок текущей страницы
        'title': 'Поставщики',
        # отображаемое на сайте имя пользователя
        'screenname': request.user.first_name or request.user.username
    }

    user_profiles = Profile.objects.filter(type=4)
    users = [User.objects.get(id=s.id) for s in user_profiles]
    context.update({'users': users})
    return TemplateResponse(request, 'manager/sellers.html', context=context)

@login_required(login_url='/accounts/login/')
def deactivate(request, uid):
    """Деактивация пользователя
    """
    if request.user.profile.type != 5:
        raise PermissionDenied

    if User.objects.filter(id=uid):
        user = User.objects.get(id=uid)
        user.is_active = False
        user.save()
        messages.info(request, 'Запрос обработан')
        return redirect('m_sellers')
    else:
        messages.warning(request, 'Данный пользователь не найден')
        return redirect('m_sellers')

@login_required(login_url='/accounts/login/')
def activate(request, uid):
    """активация пользователя
    """
    if request.user.profile.type != 5:
        raise PermissionDenied

    if User.objects.filter(id=uid):
        user = User.objects.get(id=uid)
        user.is_active = True
        user.save()
        messages.info(request, 'Запрос обработан')
        return redirect('m_sellers')
    else:
        messages.warning(request, 'Данный пользователь не найден')
        return redirect('m_sellers')

@login_required(login_url='/accounts/login/')
def prolong(request, uid):
    """Продление платного пользования сервиса
    """
    if request.user.profile.type != 5:
        raise PermissionDenied

    context = {
        # Заголовок текущей страницы
        'title': 'Поставщики: платный период',
        # отображаемое на сайте имя пользователя
        'screenname': request.user.first_name or request.user.username
    }

    if User.objects.filter(id=uid):
        user = User.objects.get(id=uid)
        context.update({'user': user})

        if request.POST:
            print(request.POST)
            period = int(request.POST.get('up'))
            if period in [1, 2, 3]:
                if period == 1:
                    t = timedelta(days=7)
                elif period == 2:
                    t = timedelta(days=30)
                else:
                    t = timedelta(days=365)
                
                bills = SystemBill.objects.filter(user=user)
                if bills.count() == 0:
                    date_start = datetime.now()
                else:
                    bills = SystemBill.objects.filter(user=user).last()
                    date_start = bills.date_end

                # https://stackoverflow.com/questions/15307623/cant-compare-naive-and-aware-datetime-now-challenge-datetime-end
                utc=pytz.UTC

                date_start_utc = date_start.replace(tzinfo=utc)
                date_now_utc = datetime.now().replace(tzinfo=utc)

                # Определяем начальную дату
                if date_start_utc < date_now_utc:
                    date_start = datetime.now()
                # Сохраняем
                SystemBill(
                    user=user,
                    date_start=date_start,
                    date_end=date_start+t,
                    amount=int(request.POST.get('amount')),
                    actor=request.user
                ).save()
                messages.info(request, 'Новый период активирован.')
                return redirect('m_sellers')
            else:
                messages.error(request, 'Передан некорректный запрос.')

        user_bills = SystemBill.objects.filter(user=user).order_by('-id')
        context.update({'bills': user_bills})
        context.update({'last': user_bills.last()})
        return TemplateResponse(request, 'manager/prolong.html', context=context)
    else:
        messages.warning(request, 'Данный пользователь не найден')
        return redirect('m_sellers')