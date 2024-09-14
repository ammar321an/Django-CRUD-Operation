from django import forms
from .models import RegistrationForm

class RegistrationFormForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), min_length=8)
    repassword = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), min_length=8)
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = RegistrationForm
        fields = ['name', 'email', 'password', 'repassword']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repassword = cleaned_data.get('repassword')

        if password and repassword and password != repassword:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data