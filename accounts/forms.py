from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={
            'class': 'pc-form-control',
            'placeholder': 'Enter your email',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'pc-form-control',
            'placeholder': 'Enter your password',
            'id': 'loginPassword',
        })
    )
    remember_me = forms.BooleanField(required=False, label='Remember me')


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'pc-form-control', 'placeholder': 'Dr. Priya Sharma'})
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'pc-form-control', 'placeholder': 'priya_sharma'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'pc-form-control', 'placeholder': 'priya@example.com'})
    )
    phone_number = forms.CharField(
        max_length=20, required=False,
        widget=forms.TextInput(attrs={'class': 'pc-form-control', 'placeholder': '+91 98765 43210'})
    )
    institution = forms.CharField(
        max_length=200, required=False,
        widget=forms.TextInput(attrs={'class': 'pc-form-control', 'placeholder': 'Indian Institute of Technology, Delhi'})
    )
    designation = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={'class': 'pc-form-control', 'placeholder': 'Research Scientist'})
    )
    user_category = forms.ChoiceField(
        choices=CustomUser.USER_CATEGORIES,
        widget=forms.Select(attrs={'class': 'pc-form-control'})
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'pc-form-control', 'placeholder': 'Create a strong password', 'id': 'regPassword1'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'pc-form-control', 'placeholder': 'Repeat your password', 'id': 'regPassword2'})
    )

    class Meta:
        model = CustomUser
        fields = ['full_name', 'username', 'email', 'phone_number',
                  'institution', 'designation', 'user_category', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email address already exists.')
        return email


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'username', 'phone_number', 'institution',
                  'designation', 'user_category', 'bio', 'profile_picture']
        widgets = {
            'full_name':     forms.TextInput(attrs={'class': 'pc-form-control'}),
            'username':      forms.TextInput(attrs={'class': 'pc-form-control'}),
            'phone_number':  forms.TextInput(attrs={'class': 'pc-form-control'}),
            'institution':   forms.TextInput(attrs={'class': 'pc-form-control'}),
            'designation':   forms.TextInput(attrs={'class': 'pc-form-control'}),
            'user_category': forms.Select(attrs={'class': 'pc-form-control'}),
            'bio':           forms.Textarea(attrs={'class': 'pc-form-control', 'rows': 4}),
            'profile_picture': forms.FileInput(attrs={'class': 'pc-form-control'}),
        }
