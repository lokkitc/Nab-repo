from django import forms
from django.contrib.auth import get_user_model

class ProfileUserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'address', 'photo']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.required = False 
            
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
    
