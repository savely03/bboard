from django import forms
from .models import AvdUser
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .models import AvdUser
from django.contrib.auth.forms import AuthenticationForm


class AvdUserForm(forms.ModelForm):
    class Meta:
        model = AvdUser
        fields = ('username', 'email', 'first_name', 'last_name', 'send_messages')


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(
        widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()

        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password2 != password2:
            errors = {'password2': ValidationError(
                'Введенные пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):

        user = super().save(commit=False)

        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta:
        model = AvdUser

        fields = ('username', 'email', 'password1', 'password2',
                  'first_name', 'last_name', 'send_messages')
