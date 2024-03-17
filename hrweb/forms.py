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


        