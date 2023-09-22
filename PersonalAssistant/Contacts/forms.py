from django import forms
from .models import Contact
import phonenumbers


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'address', 'phone_number', 'email', 'birthday']
        exclude = ['user']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        try:
            parsed_number = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise forms.ValidationError("Invalid phone number. Please enter a valid phone number.")
        except Exception:
            raise forms.ValidationError("Invalid phone number format. Please use a valid format.")
        return phone_number


class ContactDeleteForm(forms.Form):
    pass


class FeedbackForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)