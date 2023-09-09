from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'address', 'phone_number', 'email', 'birthday']


class ContactDeleteForm(forms.Form):
    pass  