from django import forms

from .models import Contact, CV


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact

        fields = ['name', 'email', 'message']


class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ['name', 'email', 'profile_picture']