from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseNotFound
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User

from webpanel.models.profile import Profile
from webpanel.models.order import Order
from webpanel.models.transporter_bill import Delivery
from webpanel.forms import ConfirmTransporterForm
from webpanel.forms import UpdateProfileTransporterForm

@login_required(login_url='/accounts/login/')
def index(request):
    """Точка входа профиля продавца
    """
    if request.user.profile.type != 3:
        raise PermissionDenied

    context = {
        # Заголовок текущей страницы
        'title': 'Сводка по вашему аккаунту',
        # отображаемое на сайте имя пользователя
        'screenname': request.user.first_name or request.user.username
    }

    # Список заказов, ожидающих доставки
    # Принимаются только оплаченные заказы
    orders = Order.objects.filter(status=4)

    context.update({'orders': orders})

    return TemplateResponse(request, 'transporter/index.html', context=context)

@login_required(login_url='/accounts/login/')
def about(request, order_number):
    """Страница о заказа на доставку
    """
    if request.user.profile.type != 3:
        raise PermissionDenied

    context = {
        # Заголовок текущей страницы
        'title': 'Заявка на доставку',
        # отображаемое на сайте имя пользователя
        'screenname': request.user.first_name or request.user.username
    }

    # проверяем, можем ли мы показать эту заявку данному пользователю
    order = Order.objects.filter(order_number=order_number)
    delivery = Delivery.objects.filter(order_number=order_number).filter(user=request.user)

    if delivery.count() == 0 and order.count() > 0:
        context.update({'creation_date': order.last().creation_date})
        context.update({'bill_date': order.last().bill_date})
        context.update({'delivery_from': order.last().product.user.profile.address})
        context.update({'delivery_to': order.last().user.profile.address})
        context.update({'order': order})
        context.update({'order_number': order_number})
        context.update({'order_status': order.last().status})
        context.update({'form': ConfirmTransporterForm()})
    else:
        messages.error(request, 'Просмотр данной заявки недоступен')
        return redirect('tr_index')
    return TemplateResponse(request, 'transporter/about.html', context=context)


@login_required(login_url='/accounts/login/')
def confirmed_order(request, order_number):
    """Подтверждённый заказ
    """
    if request.user.profile.type != 3:
        raise PermissionDenied

    context = {
        # Заголовок текущей страницы
        'title': 'Подтверждённый заказ',
        # отображаемое на сайте имя пользователя
        'screenname': request.user.first_name or request.user.username
    }

    if request.POST:
        # новый заказ выбран транспортником на подтверждение
        order = Order.objects.filter(status=4).filter(order_number=order_number)
        delivery = Delivery.objects.filter(order_number=order_number).filter(user=request.user)
        if delivery.count() == 0 and order.count() > 0:
            # заказ открыт, оформляем его на транспортника
            form = ConfirmTransporterForm(data=request.POST)
            if form.is_valid():
                order.status = 3
                order.delivery_date = datetime.now()
                order.update()
                delivery = Delivery(
                    user=request.user,
                    order_number=order.last().order_number,
                    amount=form.cleaned_data.get('price')
                    )
                delivery.save()
                messages.success(request, 'Поздравляем! Теперь это ваш заказ на доставку!')
            else:
                messages.error(request, 'Проверьте правильность заполнения формы.')
                return redirect('tr_about', order_number=order_number)
        else:
            messages.error(request, 'Подтрерждение невозможно: Данная заявка недоступна для транспортных услуг.')
            return redirect('tr_index')

    # выводим данные по заказу
    if Delivery.objects.filter(order_number=order_number).filter(user=request.user):
        delivery = Delivery.objects.get(order_number=order_number)
        order = Order.objects.filter(order_number=order_number)
        context.update({'delivery': delivery})
        context.update({'order': order})

        context.update({'creation_date': order.last().creation_date})
        context.update({'delivery_date': order.last().delivery_date})
        context.update({'delivery_from': order.last().product.user.profile.address})
        context.update({'delivery_to': order.last().user.profile.address})
        context.update({'delivery_to': order.last().user.profile.address})
        context.update({'seller_phone': order.last().product.user.profile.phone})
        context.update({'user_phone': order.last().user.profile.phone})
    else:
        messages.error(request, 'Данная заявка не найдена или вы не имеете к ней доступа.')
        return redirect('tr_index')

    return TemplateResponse(request, 'transporter/confirmed_order.html', context=context)


@login_required(login_url='/accounts/login/')
def close_order(request, order_number):
    """Закрывает заявку
    """
    if request.user.profile.type != 3:
        raise PermissionDenied

    if Delivery.objects.filter(order_number=order_number).filter(user=request.user):
        Order.objects.filter(order_number=order_number).update(status=6)
        messages.info(request, 'Заявка закрыта.')
        return redirect('tr_index')
    else:
        messages.info(request, 'Данная заявка не найдена или вы не имеете к ней доступа.')
        return redirect('tr_index')

@login_required(login_url='/accounts/login/')
def requisites(request):
    """Реквизиты
    """
    if request.user.profile.type != 3:
        raise PermissionDenied

    context = {
        # Заголовок текущей страницы
        'title': 'Реквизиты',
        # отображаемое на сайте имя пользователя
        'screenname': request.user.first_name or request.user.username
    }

    if request.method == "POST":
        form = UpdateProfileTransporterForm(data=request.POST, instance=request.user.profile)
        if form.is_valid():
            # Проверка
            phone = form.cleaned_data.get('phone')
            check_phone = Profile.objects.filter(phone=phone).exclude(user=request.user)

            if check_phone.count() == 0:
                bin = form.cleaned_data.get('bin')
                check_bin = Profile.objects.filter(bin=bin).exclude(user=request.user)

                if check_bin.count() == 0:
                    request.user.profile.phone = form.cleaned_data.get('phone')
                    request.user.profile.company_name = form.cleaned_data.get('company_name')
                    request.user.profile.address = form.cleaned_data.get('address')
                    request.user.profile.bin = form.cleaned_data.get('bin')
                    request.user.profile.bank_account = form.cleaned_data.get('bank_account')
                    request.user.save()
                    messages.success(request, 'Реквизиты вашей организации обновлены.')
                else:
                    messages.error(request, 'Данный БИН нельзя использовать.')
            else:
                messages.error(request, 'Данный номер телефона нельзя использовать.')

    form = UpdateProfileTransporterForm(instance=request.user.profile)
    context.update({'form':form})
    return TemplateResponse(request, 'transporter/requisites.html', context=context)


@login_required(login_url='/accounts/login/')
def payment(request):
    """Оплата сервиса
    """
    if request.user.profile.type != 3:
        raise PermissionDenied

    context = {
        # Заголовок текущей страницы
        'title': 'Оплата сервиса',
        # отображаемое на сайте имя пользователя
        'screenname': request.user.first_name or request.user.username
    }
    return TemplateResponse(request, 'transporter/payment.html', context=context)

@login_required(login_url='/accounts/login/')
def delivery_list(request):
    """Список взятых транспортником доставок
    """
    if request.user.profile.type != 3:
        raise PermissionDenied

    context = {
        # Заголовок текущей страницы
        'title': 'Список ваших доставок',
        # отображаемое на сайте имя пользователя
        'screenname': request.user.first_name or request.user.username
    }

    deliveries = Delivery.objects.filter(user=request.user)

    deliveries_list = []
    for i in deliveries:
        d = {
            'order_number': i.order_number,
            'amount': i.amount,
            'order': Order.objects.filter(order_number=i.order_number).last()
        }
        deliveries_list.append(d)
    context.update({'deliveries_list': deliveries_list})

    return TemplateResponse(request, 'transporter/delivery_list.html', context=context)