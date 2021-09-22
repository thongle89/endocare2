from django import forms 
from django.forms import ModelForm
from .models import Pending


class PendingForm(ModelForm):
	class Meta: #django declare
		model = Pending
		# fields = "__all__" #option 1
		# name,event_date,venue,manager,description,attendees
		fields = ('dealer','type_s','tr_date','quotation_date','part_list_date','repair_note',
					'p_status','p_score','superadmin')
		labels={
			# 'rma_id':'RMA:',
			'dealer':'Đại lý',
			'type_s': 'Kiểu Thiết bị',
			'tr_date':'Ngày giám định',
			'part_list_date': 'Ngày Xuất linh kiện',
			'quotation_date':'Ngày báo giá',
			'repair_note':'Note',
			'p_status':'Status',
			'p_score':'Score',
			'superadmin':'Super Admin'
			
		}
		widgets ={
			# 'rma_id':forms.TextInput(attrs={'class':'form-control','placeholder':'RMA'}),

			'dealer':forms.Select(attrs={'class':'form-select','placeholder':'Đại lý'}), 
			'type_s':forms.TextInput(attrs={'class':'form-control','placeholder':'Kiểu Thiết bị'}), 
			'tr_date':forms.DateInput(attrs={'class':'form-control','placeholder':''}),
			'part_list_date':forms.DateInput(attrs={'class':'form-control','placeholder':''}),
			'quotation_date':forms.DateInput(attrs={'class':'form-control','placeholder':''}),
			'repair_note':forms.Textarea(attrs={'class':'form-control','placeholder':''}),
			'p_status':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
			'p_score':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
			'superadmin':forms.CheckboxInput(),

			

			# 'rma_id__repair_size':forms.TextInput(attrs={'class':'form-control','placeholder':''}),


		}
