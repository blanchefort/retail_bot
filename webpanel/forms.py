from django import forms
from django.contrib.auth.models import User
from webpanel.models.profile import Profile
from webpanel.models.price_list import PriceLists
from django.core.validators import FileExtensionValidator

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