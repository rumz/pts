from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory

from .models import Category, Ticket, Comment

class LogInForm(forms.Form):
    userID = forms.CharField(
                                label = '',
                                widget = forms.TextInput(attrs = {'placeholder':'Employee ID Number'}),
                                required = True,
                            )

    password = forms.CharField(
                                label = '',
                                widget = forms.PasswordInput(attrs = {'placeholder':'Password'}),
                                required = True,
                            )


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )

class ChangePass(forms.Form):
        current_password = forms.CharField(required=True,
                                           widget = forms.PasswordInput(attrs={
                                                   'class':'form-control',
                                                   'placeholder':'Current Password',
                                                   'required':'True'
                                           }),
        )

        new_password = forms.CharField(required=True,
                                           widget = forms.PasswordInput(attrs={
                                                   'class':'form-control',
                                                   'placeholder':'New Password',
                                                   'required':'True'
                                           }),
        )

        confirm_password = forms.CharField(required=True,
                                           widget = forms.PasswordInput(attrs={
                                                   'class':'form-control',
                                                   'placeholder':'Confirm Password',
                                                   'required':'True'
                                           }),
        )
