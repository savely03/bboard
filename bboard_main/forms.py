from django import forms
from django.forms import inlineformset_factory
from .models import AvdUser, Bb, AdditionalImage
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from .models import SuperRubric, SubRubric


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


class SubRubricForm(forms.ModelForm):
    super_rubric = forms.ModelChoiceField(queryset=SuperRubric.objects.all(), empty_label=None, label='Надрубрика',
                                          required=True)

    class Meta:
        model = SubRubric
        fields = '__all__'


class SearchForm(forms.Form):
    keyword = forms.CharField(required=False, max_length=20, label='')


class BbForm(forms.ModelForm):
    class Meta:
        model = Bb
        fields = '__all__'
        widgets = {'author': forms.HiddenInput}


AiFormSet = inlineformset_factory(Bb, AdditionalImage, fields='__all__')



