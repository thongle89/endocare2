from django import forms 
from django.forms import ModelForm
from .models import Pending
from whiteboard.models import Comment

class PendingForm(ModelForm):
	class Meta: #django declare
		model = Pending
		# fields = "__all__" #option 1
		# name,event_date,venue,manager,description,attendees
		fields = ('dealer','type_s','tr_date','quotation_date','confirm_date','return_date','part_list_date','repair_note',
					'p_status','p_score','superadmin')
		labels={
			# 'rma_id':'RMA:',
			'dealer':'Đại lý',
			'type_s': 'Kiểu Thiết bị',
			'tr_date':'Ngày giám định',
			'part_list_date': 'Ngày Xuất linh kiện',
			'quotation_date':'Ngày báo giá',
			'confirm_date':'Ngày Khách hàng xác nhận sửa chữa',
			'return_date':'Ngày trả dây',
			'repair_note':'Note',
			'p_status':'Status',
			'p_score':'Score',
			'superadmin':'Super Admin'
			
		}
		widgets ={
			# 'rma_id':forms.TextInput(attrs={'class':'form-control','placeholder':'RMA'}),

			'dealer':forms.Select(attrs={'class':'form-select','placeholder':'Đại lý'}), 
			'type_s':forms.TextInput(attrs={'class':'form-control','placeholder':'Kiểu Thiết bị'}), 
			'tr_date':forms.widgets.DateInput(attrs={'type':'date','class':'form-control','placeholder':''}),
			'part_list_date':forms.widgets.DateInput(attrs={'type':'date','class':'form-control','placeholder':''}),
			# 'quotation_date':forms.DateInput(attrs={'class':'form-control','placeholder':''}),
			'quotation_date':forms.widgets.DateInput(attrs={'type':'date','class':'form-control','placeholder':''}),
			'confirm_date':forms.widgets.DateInput(attrs={'type':'date','class':'form-control','placeholder':''}),
			'return_date':forms.widgets.DateInput(attrs={'type':'date','class':'form-control','placeholder':''}),
			'repair_note':forms.Textarea(attrs={'class':'form-control','placeholder':''}),
			'p_status':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
			'p_score':forms.TextInput(attrs={'class':'form-control','placeholder':''}),
			'superadmin':forms.CheckboxInput(),


		}
class CommentForm(ModelForm):
    class Meta: #django declare
        model = Comment
        fields = "__all__" #option 1
        # name,event_date,venue,manager,description,attendees
        # fields = ('rma_id','username','cmt_text',)
        labels={
            'cmt_text':'',
        }
        widgets ={
            'cmt_text':forms.Textarea(attrs={'class':'form-control','placeholder':'Viết Phản Hồi'}),
            
        }

