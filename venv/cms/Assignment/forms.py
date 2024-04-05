from django import forms
from django.contrib.auth.forms import UserCreationForm
from Assignment.models import User, Content

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'address', 'city', 'state', 'country', 'pincode']
        widgets = {
            'password': forms.PasswordInput(),
        }

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['title', 'body', 'summary', 'categories']

class SearchForm(forms.Form):
    search_term = forms.CharField(max_length=255, required=False)
