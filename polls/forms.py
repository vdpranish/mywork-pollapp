from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfileImg, UserRole


class CreateUser(UserCreationForm):
    password2 = None
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            # 'email':forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}))
            # 'password1': forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

        }


# login form
class LoginUser(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_password(self):
        password_passed = self.cleaned_data.get('password')
        username = self.cleaned_data.get('username')

        qs = User.objects.filter(username=username)
        if not qs[0].password  in password_passed:
            return  forms.ValidationError('incorrect Password ')


class ProfileImgForm(forms.ModelForm):
    class Meta:
        model = UserProfileImg
        fields = ['picture']


class UserRoleForm(forms.ModelForm):
    class Meta:
        model = UserRole
        fields = ['role']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'})

        }
