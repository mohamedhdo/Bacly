from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
from core.constants import STREAMS


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"placeholder": "First Name"}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"placeholder": "Last Name"}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"placeholder": "Email address"}))
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, initial="student")
    stream = forms.ChoiceField(choices=User.STREAM_CHOICES, initial="Mathematics")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email", "role", "stream")


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "stream", "bac_date")
        widgets = {
            "bac_date": forms.DateInput(attrs={"type": "date"}),
        }


class JoinClassForm(forms.Form):
    join_code = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            "placeholder": "6-char code (e.g. BAC26M)",
            "class": "uppercase tracking-widest text-center font-bold text-lg",
            "maxlength": 6
        })
    )
