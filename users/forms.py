# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,SetPasswordForm,PasswordResetForm
from django.contrib.auth import get_user_model
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
import re
from django.core.exceptions import ValidationError

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='A valid email address, please.', required=True)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match('^[a-zA-Z ]+$', first_name):
            raise forms.ValidationError('First name should only contain text characters.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match('^[a-zA-Z ]+$', last_name):
            raise forms.ValidationError('Last name should only contain text characters.')
        return last_name
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError('Password should be at least 8 characters.')
        if not re.search('[A-Z]', password1):
            raise forms.ValidationError('Password should have at least one uppercase letter.')
        if not re.search('[^A-Za-z0-9]', password1):
            raise forms.ValidationError('Password should have at least one special character.')
        return password1
    
    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        if len(password2) < 8:
            raise forms.ValidationError('Password should be at least 8 characters.')
        if not re.search('[A-Z]', password2):
            raise forms.ValidationError('Password should have at least one uppercase letter.')
        if not re.search('[^A-Za-z0-9]', password2):
            raise forms.ValidationError('Password should have at least one special character.')
        return password2

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Password and confirm password do not match.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username or Email'}),
        label="Username or Email*")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))   

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email' ]

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name:
            raise ValidationError("First name is required")
        if not first_name.isalpha():
            raise ValidationError("First name should contain only letters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name:
            raise ValidationError("Last name is required")
        if not last_name.isalpha():
            raise ValidationError("Last name should contain only letters.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise ValidationError("Email is required")
        if get_user_model().objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Email already exists.")
        return email

    
        

class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('new_password1')
        if len(password1) < 8:
            raise forms.ValidationError("Password should be at least 8 characters long.")
        if not re.search("[A-Z]", password1):
            raise forms.ValidationError("Password should have at least one uppercase letter.")
        if not re.search("[^A-Za-z0-9]", password1):
            raise forms.ValidationError("Password should have at least one special symbol.")
        return cleaned_data  


class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    