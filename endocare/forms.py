from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm
from django import forms 
from django.contrib.auth import get_user_model

User = get_user_model()
class UserPasswordResetForm(PasswordResetForm):
    
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)


    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nhập Email bạn đã đăng ký',
        'type': 'email',
        'name': 'email'
        }))

class resetPasswordForm(SetPasswordForm):
    
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), 
    label="Mật khẩu mới")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), 
    label="Xác nhận mật khẩu")

    class Meta:
        model = User
        fields = ("new_password1", "new_password2")
