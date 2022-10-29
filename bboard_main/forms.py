from django import forms
from .models import AvdUser


class AvdUserForm(forms.ModelForm):
    class Meta:
        model = AvdUser
        fields = ('username', 'email', 'first_name', 'last_name', 'send_messages')
