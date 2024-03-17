from django import forms
from .models import CustomUser, Vacancy

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        
class VacancyForm(forms.ModelForm):
    
    
    class Meta:
        model = Vacancy
        fields = {
            'name',
            'employer',
            'url',
            'salary',
            'description',
            'area',
            'date'
        }


class ProfileUpdateForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    username = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)

class PasswordChangeForm(forms.Form):
    newpass = forms.CharField(widget=forms.PasswordInput, required=True)
    oldpass = forms.CharField(widget=forms.PasswordInput, required=True)
    rnewpass = forms.CharField(widget=forms.PasswordInput, required=True)
        