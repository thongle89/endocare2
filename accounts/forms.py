from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django import forms 
from django.forms import ModelForm
from django.contrib.auth import get_user_model

User = get_user_model()
# from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

	class Meta:
		model = CustomUser 
		fields = "__all__"

class RegisterUserForm(UserCreationForm):
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}),label ='Email(*):',help_text='Cung cấp email dùng để xác thực tài khoản.')
	full_name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}),label='Họ Và Tên(*)')
	phone = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}),label='Số Điện Thoại(*)')
	organization = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}),label='Tên Đơn vị/Tổ chức/Bệnh viện/Phòng Khám(*)',help_text='Cung cấp tên đơn vị để chúng tôi chăm sóc bạn tốt hơn.')

	help_texts = {
		'organization':'Cung cấp tên đơn vị của bạn để chúng tôi chăm sóc tốt hơn.',
		'email': 'Cung cấp email dùng để xác thực tài khoản.',
	}
	class Meta:
		model = User
		fields = ('username','full_name','email','phone','organization','password1','password2')
		help_texts = {
		'username':'Chỉ chấp nhận ký tự thường từ a->z,số 0->9. Viết liền không dấu.',
		
		
		}
		labels ={
		'username': 'Tên Đăng Nhập(*)',
		
		 
		}
	
	
	def __init__(self,*args,**kwargs):
		super(RegisterUserForm,self).__init__(*args,**kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['class'] = 'form-control'

		self.fields['password1'].label = 'Mật khẩu(*)'
		self.fields['password2'].label = 'Xác nhận mật khẩu(*)'

		self.fields['password1'].help_text = 'Mật khẩu tối thiểu 8 ký tự, bao gồm cả chữ và số, không được trùng với tên đăng nhập.'
		self.fields['password2'].help_text = 'Nhập mật khẩu tương tự như trên để xác minh'
			