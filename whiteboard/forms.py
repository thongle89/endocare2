from django.forms import ModelForm
from .models import Event
from django.contrib.auth import get_user_model
from django import forms
User = get_user_model()
#create a venue form
class EventForm(ModelForm):
	class Meta: #django declare
		model = Event
		# fields = "__all__" #option 1
		# name,event_date,venue,manager,description,attendees
		fields = ('type_e','name', 'event_date', 'venue', 'manager','attendees', 'description')
		labels={
			'name': '',
			'event_date':'',
			'venue':'Venue:',
			'manager':'Manager:',
			'attendees':'Attendees:',
			'description':'',
		}
		widgets ={
			'type_e':forms.Select(attrs={'class':'form-select','placeholder':'Venue'}),
			'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Event Name'}),
			'event_date':forms.DateInput(attrs={'type':'date','class':'form-control','placeholder':'Event Date'}),
			'venue':forms.Select(attrs={'class':'form-select','placeholder':'Venue'}),
			'manager':forms.Select(attrs={'class':'form-select','placeholder':'Manager'}),
			'attendees':forms.SelectMultiple(attrs={'class':'form-control','placeholder':'Attendees'}),
			'description':forms.Textarea(attrs={'class':'form-control','placeholder':'Description'}),
			
		}
class VerifyUserForm(ModelForm):
	class Meta:
		model = User
		fields = ('username','full_name','phone','email','is_ffvn','dealer','customer')
		labels={
			'username':'Tên Đăng Nhập',
			'full_name':'Họ Tên',
			'phone':'Điện Thoại',
			'email':'Email',
			'is_ffvn':'FFVN members',
			'dealer':'Nhà Phân Phối',
			'customer':'Khách hàng',
		}
		widgets ={
			'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Tên Đăng nhâp'}),
			'full_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Họ Tên'}),
			'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'Điện Thoại'}),
			'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),
			'is_ffvn':forms.CheckboxInput(),
			'dealer':forms.Select(attrs={'class':'form-select','placeholder':'Nhà Phân Phối'}),
			'customer':forms.Select(attrs={'class':'form-select','placeholder':'Khách Hàng'}),
		}

