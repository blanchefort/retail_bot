from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from webpanel.forms import UserForm, ProfileUserForm
from webpanel.forms import ProfileTransporterForm, ProfileSellerForm
from webpanel.models.product import Product
from webpanel.models.profile import Profile

def index(request):
    """Стартовая страница
    """
    products_count = Product.objects.filter(is_active=True).count()
    sellers_count = Profile.objects.filter(type=4).count()
    transporters_count = Profile.objects.filter(type=3).count()
    user_1 = Profile.objects.filter(type=1).count()
    user_2 = Profile.objects.filter(type=2).count()
    users_count = int(user_1) + int(user_2)

    context = {
        'products_count': products_count,
        'sellers_count': sellers_count,
        'transporters_count': transporters_count,
        'users_count': users_count
    }

    return TemplateResponse(request, 'index.html', context=context)


def select_profile(request):
    """Выбор профиля пользователя в зависимости от его типа
    """
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin:index')
        if request.user.profile.type == 1:
            # Бесплатный пользователь
            pass
        elif request.user.profile.type == 2:
            # Платный пользователь
            pass
        elif request.user.profile.type == 3:
            # Транспортник
            return redirect('tr_index')
        elif request.user.profile.type == 4:
            # Продавец
            return redirect('seller_index')
        elif request.user.profile.type == 5:
            # Менеджер сервиса
            pass
        else:
            raise PermissionDenied

    return redirect('index')


def select_registration(request):
    """Выбор типа регистрации
    """
    if request.user.is_authenticated:
        return redirect(index.select_profile())

    return TemplateResponse(request, 'registration/select_type.html')


def registration(request, type):
    """Регистрация пользователя
    """
    title = None
    if request.user.is_authenticated:
        return redirect(index.select_profile())

    if type == 1:
        # Покупатель
        if request.method == 'POST':
            user_form = UserForm(request.POST)
            profile_form = ProfileUserForm(request.POST)
            if user_form.is_valid() and profile_form.is_valid():
                new_user = user_form.save()
                new_user.set_password(new_user.password)
                new_user.profile.type = type
                new_user.profile.phone = profile_form.cleaned_data.get('phone')
                new_user.save()
                messages.success(request, 'Поздравляем! Вы успешно зарегистраровались!')
                return redirect('login')
            else:
                messages.error(request, 'Пожалуйста, заполните все поля корректно.')
        else:
            title = 'Регистрация в качестве покупателя'
            user_form = UserForm()
            profile_form = ProfileUserForm()
    elif type == 3:
        # Транспортник
        if request.method == 'POST':
            user_form = UserForm(request.POST)
            profile_form = ProfileTransporterForm(request.POST)
            if user_form.is_valid() and profile_form.is_valid():
                new_user = user_form.save()
                new_user.set_password(new_user.password)
                new_user.profile.type = type
                new_user.profile.phone = profile_form.cleaned_data.get('phone')
                new_user.profile.company_name = profile_form.cleaned_data.get('company_name')
                new_user.profile.address = profile_form.cleaned_data.get('address')
                new_user.profile.bin = profile_form.cleaned_data.get('bin')
                new_user.profile.bank_account = profile_form.cleaned_data.get('bank_account')
                new_user.save()
                messages.success(request, 'Поздравляем! Вы успешно зарегистраровались!')
                return redirect('login')
            else:
                messages.error(request, 'Пожалуйста, заполните все поля корректно.')
        else:
            title = 'Регистрация в качестве транспортника'
            user_form = UserForm()
            profile_form = ProfileTransporterForm()
    elif type == 4:
        # Продавец
        if request.method == 'POST':
            user_form = UserForm(request.POST)
            profile_form = ProfileSellerForm(request.POST)
            if user_form.is_valid() and profile_form.is_valid():
                new_user = user_form.save()
                new_user.set_password(new_user.password)
                new_user.profile.type = type
                new_user.profile.phone = profile_form.cleaned_data.get('phone')
                new_user.profile.company_name = profile_form.cleaned_data.get('company_name')
                new_user.profile.address = profile_form.cleaned_data.get('address')
                new_user.profile.bin = profile_form.cleaned_data.get('bin')
                new_user.profile.bank_account = profile_form.cleaned_data.get('bank_account')
                new_user.save()
                messages.success(request, 'Поздравляем! Вы успешно зарегистраровались!')
                return redirect('login')
            else:
                messages.error(request, 'Пожалуйста, заполните все поля корректно.')
        else:
            title = 'Регистрация в качестве продавца'
            user_form = UserForm()
            profile_form = ProfileSellerForm()
    else:
        messages.error(request, 'Выберите пункт из списка ниже!')
        return redirect('select_registration')

    return TemplateResponse(
        request,
        'registration/registration.html',
        {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': title
    })