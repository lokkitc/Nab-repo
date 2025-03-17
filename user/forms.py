from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', "first_name", "last_name")
        labels = {
            'email': 'Email',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password1'] != cd['password2']:
                raise forms.ValidationError('Пароли не совпадают')
            return cd['password2']


        def clean_email(self):
            email = self.cleaned_data['email']
            if get_user_model().objects.filter(email=email).exists():
                raise forms.ValidationError('Пользователь с таким email уже существует')
            return email


class ProfileUserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.required = False  # делаем поля необязательными
            
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if get_user_model().objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Этот email уже используется')
        return email
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            if get_user_model().objects.filter(username=username).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Это имя пользователя уже занято')
        return username
    

class UserPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['old_password', 'new_password1', 'new_password2']
