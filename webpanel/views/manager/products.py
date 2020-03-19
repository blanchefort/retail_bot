"""Менеджмент товаров
"""
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseNotFound
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from webpanel.models.product_category import ProductCategory
from webpanel.models.product_unit_type import ProductUnitType
from webpanel.models.product import Product

from webpanel.forms import CategoryForm


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

@login_required(login_url='/accounts/login/')
def categories(request):
    """Список категорий товаров
    """
    if request.user.profile.type != 5:
        raise PermissionDenied

    context = {
        # Заголовок текущей страницы
        'title': 'Категории товаров',
        # отображаемое на сайте имя пользователя
        'screenname': request.user.first_name or request.user.username
    }

    # Изменяем названия категорий
    if request.POST:
        count = ProductCategory.objects.all().count()
        for cat in range(1, count+1):
            new_name = request.POST.get(f'category_{cat}')
            if ProductCategory.objects.filter(id=cat) and len(new_name) > 0:
                category = ProductCategory.objects.get(id=cat)
                category.name = new_name
                category.save()

    categories = ProductCategory.objects.all()

    context.update({'categories': categories})

    return TemplateResponse(request, 'manager/categories.html', context=context)

@login_required(login_url='/accounts/login/')
def add_new_category(request):
    """Добавление новой категории
    """
    if request.user.profile.type != 5:
        raise PermissionDenied

    context = {
        # Заголовок текущей страницы
        'title': 'Добавить новую категорию',
        # отображаемое на сайте имя пользователя
        'screenname': request.user.first_name or request.user.username
    }

    if request.POST:
        form = CategoryForm(request.POST)
        if form.is_valid:
            form.save()
            messages.info(request, 'Категория добавлена.')
            return redirect('m_categories')

    context.update({'form': CategoryForm()})

    return TemplateResponse(request, 'manager/add_new_category.html', context=context)

@login_required(login_url='/accounts/login/')
def units(request):
    """Единицы измерения товаров
    """
    if request.user.profile.type != 5:
        raise PermissionDenied

    context = {
        # Заголовок текущей страницы
        'title': 'Единицы измерения товаров',
        # отображаемое на сайте имя пользователя
        'screenname': request.user.first_name or request.user.username
    }

    #Редактируем единицы измерения
    if request.POST:
        count = ProductUnitType.objects.all().count()
        for u in range(1, count+1):
            new_name = request.POST.get(f'name_{u}')
            new_short = request.POST.get(f'short_{u}')
            if ProductUnitType.objects.filter(id=u):
                unit = ProductUnitType.objects.get(id=u)
                unit.name = new_name
                unit.short = new_short
                unit.save()
        messages.info(request, 'Запрос обработан.')

    units = ProductUnitType.objects.all()
    context.update({'units': units})
    return TemplateResponse(request, 'manager/units.html', context=context)

@login_required(login_url='/accounts/login/')
def products(request):
    """Список товаров
    """
    if request.user.profile.type != 5:
        raise PermissionDenied

    context = {
        # Заголовок текущей страницы
        'title': 'Товары',
        # отображаемое на сайте имя пользователя
        'screenname': request.user.first_name or request.user.username
    }

    if request.POST:
        # В PostgreSQL можно делать более совершенный поиск
        # https://docs.djangoproject.com/en/3.0/topics/db/search/
        query = request.POST.get('q').strip().lower()
        list = Product.objects.filter(is_active=True).filter(title__icontains=query)
    else:
        list = Product.objects.filter(is_active=True).order_by('title')
        query = None

    paginator = Paginator(list, 10)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    context.update({'products': products})
    context.update({'count': list.count()})
    context.update({'query': query})
    return TemplateResponse(request, 'manager/products.html', context=context)