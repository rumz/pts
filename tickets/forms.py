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

							
# class TicketForm(forms.ModelForm):

#   def clean(self):
#     return self.cleaned_data

#   class Meta:
#     model = Ticket

#   def __init__(self, *args, **kwargs):

#     if kwargs.get('instance'):
#       subject = kwargs['instance'].subject
#       kwargs.setdefault('initial', {})['subject'] = ''

#     return super(TicketForm, self).__init__(*args, **kwargs)
