from django import forms
from django.contrib.auth.models import User
from .models import Book


class BookForm(forms.ModelForm):
    """Form for creating and updating Book instances"""
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'description', 'quote', 'cover']


class UserRegistrationForm(forms.ModelForm):
    """Form for registering a new user"""
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput
    )
    password_confirmation = forms.CharField(
        label='Підтвердження паролю',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            raise forms.ValidationError('Паролі не співпадають.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    """Form for logging in existing users"""
    username = forms.CharField(label='Ім’я користувача')
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput
    )
