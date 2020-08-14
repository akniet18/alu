from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import *


class LoginForm(forms.Form):
	phone = forms.IntegerField(label = 'phone')
	password = forms.CharField(widget = forms.PasswordInput)


class VerifyForm(forms.Form):
	key = forms.IntegerField(label = 'otp')


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    password2 = forms.CharField(widget = forms.PasswordInput)

    class Meta:
        model = User
        fields=('phone',)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        q = User.objects.filter(phone=phone)
        if q.exists():
            raise forms.ValidationError("phone is already exists")
        return phone

    def clean_password(self):
        password = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("passwords don't match")
        return password


class TempRegisterForm(forms.Form):
    phone = forms.IntegerField()
    otp = forms.IntegerField()

class SetPasswordForm(forms.Form):
    password = forms.CharField(label="passwrd", widget=forms.PasswordInput)
    password2 = forms.CharField(label="password2", widget=forms.PasswordInput)


class UserAdminCreationForm(forms.ModelForm):
    password = forms.CharField(label="passwrd", widget=forms.PasswordInput)
    password2 = forms.CharField(label="password2", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone',)


    def cleaned_password2(self):
        password = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("passwords don't match")
        return password

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('phone', 'password')

    def clean_password(self):
        return self.initial['password']


