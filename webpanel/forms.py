from django import forms
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from webpanel.models.profile import Profile
from webpanel.models.price_list import PriceLists
from webpanel.models.seller_bill import SellerBill
from webpanel.models.product_category import ProductCategory

class UserForm(forms.ModelForm):
    """Форма создания нового пользователя
    """
    #password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Данный электронный адрес уже имеется в системе.')
        return email



class ProfileUserForm(forms.ModelForm):
    """Форма создания простого пользователя (покупателя)
    """
    class Meta:
        model = Profile
        fields = ('phone',)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if Profile.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Данный номер телефона уже зарегистрирован.')
        return phone


class ProfilePaidUserForm(forms.ModelForm):
    """Форма создания платного пользователя (покупателя)
    """
    class Meta:
        model = Profile
        fields = ('phone', 'company_name', 'address', 'bin', 'bank_account',)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if Profile.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Данный номер телефона уже зарегистрирован.')
        return phone

    def clean_company_name(self):
        company_name = self.cleaned_data.get('company_name')
        if Profile.objects.filter(company_name=company_name).exists():
            raise forms.ValidationError('Данное наименование организации уже зарегистрировано.')
        return company_name

    def clean_bin(self):
        bin = self.cleaned_data.get('bin')
        if Profile.objects.filter(bin=bin).exists():
            raise forms.ValidationError('Данный БИН уже зарегистрирован в системе.')
        return bin


class ProfileTransporterForm(forms.ModelForm):
    """Форма создания транспортника
    """
    class Meta:
        model = Profile
        fields = ('phone', 'company_name', 'address', 'bin', 'bank_account',)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if Profile.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Данный номер телефона уже зарегистрирован.')
        return phone

    def clean_company_name(self):
        company_name = self.cleaned_data.get('company_name')
        if Profile.objects.filter(company_name=company_name).exists():
            raise forms.ValidationError('Данное наименование организации уже зарегистрировано.')
        return company_name

    def clean_bin(self):
        bin = self.cleaned_data.get('bin')
        if Profile.objects.filter(bin=bin).exists():
            raise forms.ValidationError('Данный БИН уже зарегистрирован в системе.')
        return bin

class UpdateProfileTransporterForm(forms.ModelForm):
    """Форма обновления продавца
    """
    class Meta:
        model = Profile
        fields = ('phone', 'company_name', 'address', 'bin', 'bank_account',)


class ProfileSellerForm(forms.ModelForm):
    """Форма создания продавца
    """
    class Meta:
        model = Profile
        fields = ('phone', 'company_name', 'address', 'bin', 'bank_account',)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if Profile.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Данный номер телефона уже зарегистрирован.')
        return phone

    def clean_company_name(self):
        company_name = self.cleaned_data.get('company_name')
        if Profile.objects.filter(company_name=company_name).exists():
            raise forms.ValidationError('Данное наименование организации уже зарегистрировано.')
        return company_name

    def clean_bin(self):
        bin = self.cleaned_data.get('bin')
        if Profile.objects.filter(bin=bin).exists():
            raise forms.ValidationError('Данный БИН уже зарегистрирован в системе.')
        return bin

class UpdateProfileSellerForm(forms.ModelForm):
    """Форма обновления продавца
    """
    class Meta:
        model = Profile
        fields = ('phone', 'company_name', 'address', 'bin', 'bank_account',)


class UploadFileForm(forms.ModelForm):
    """Форма загрузки прайс-листа
    """
    file_name = forms.FileField(
        label='Загрузить прайс-лист',
        validators=[FileExtensionValidator(['xlsx'])]
    )

    class Meta:
        model = PriceLists
        fields = ('file_name',)


class UploadBillForm(forms.ModelForm):
    """Форма загрузки прайс-листа
    """
    file_name = forms.FileField(
        label='Загрузить счёт на оплату',
        validators=[FileExtensionValidator(['xlsx', 'xls', 'ods'])]
    )

    class Meta:
        model = SellerBill
        fields = ('file_name',)


class ConfirmTransporterForm(forms.Form):
    """Подтверждение транспортником заказа,
    указание стоимости доставки.
    """
    price = forms.CharField(label='Укажите ваши стоимость доставки')


class CategoryForm(forms.ModelForm):
    """Создание новой категории товаров менеджером
    """
    class Meta:
        model = ProductCategory
        fields = ('name',)
