from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Pending,Part,Rcode,Device
from .forms import PendingForm
from django.core.paginator import Paginator
#import User table from member
from django.contrib.auth import get_user_model
from django.http import HttpResponse
import xlwt
import datetime
User = get_user_model()

from whiteboard.models import Event

def devices_xls(request):
	try:
		user_login = User.objects.get(username=request.user)
		if user_login.is_ffvn:
			devices= Device.objects.all().values_list('customer__web_name','type_s','model','serial','installed_date','warranty_date', \
							'last_repair_date')
			columns=['Khách Hàng','Loại Máy','Kiểu Máy','Số Máy','Ngày Lắp Đặt','Ngày Hết Bảo Hành',
			'Ngày sửa chữa gần nhất']
			customer_name ='All'
		elif user_login.customer != None:
			devices = Device.objects.filter(customer=user_login.customer).values_list('type_s','model','serial','installed_date','warranty_date', \
							'last_repair_date')
			columns=['Loại Máy','Kiểu Máy','Số Máy','Ngày Lắp Đặt','Ngày Hết Bảo Hành',
			'Ngày sửa chữa gần nhất']
			customer_name = user_login.customer

	except:
		pass


	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition']='attachment; filename=ThietBi_' + \
				str(customer_name) + '_' + str(datetime.date.today()) + '.xls'
	
	wb = xlwt.Workbook(encoding = 'utf-8')
	ws = wb.add_sheet('Thiết Bị')
	row_num = 0
	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	

	for col_num in range(len(columns)):
		ws.write(row_num,col_num,columns[col_num],font_style)

	font_style = xlwt.XFStyle()
	


	#Designate The Model
	# if customer_name == 'None':
	# 	devices= Device.objects.all().values_list('customer__web_name','type_s','model','serial','installed_date','warranty_date', \
	# 						'last_repair_date')
	# else:
	# 	devices = Device.objects.filter(customer=customer_name).values_list('type_s','model','serial','installed_date','warranty_date', \
	# 						'last_repair_date')

	for device in devices:
		row_num+=1

		for col_num in range(len(device)):
			if str(device[col_num]) != 'None':
				ws.write(row_num,col_num,str(device[col_num]),font_style)
	wb.save(response)
	
	return response

	
	
	

def update_pending(request,rma_id):
	pending = Pending.objects.get(rma_id=rma_id)
	form = PendingForm(request.POST or None,instance=pending)
	# instance: lấy mẫu cũ\
	rma = pending.rma_id
	sn = pending.rma_id.sn
	if form.is_valid():
		form.save()
		
		messages.success(request,('Cập nhật thành công.'))
		return redirect('quick-search',rma,sn)
	# else:
	# 	return redirect('quick-search',rma,sn)
	return render(request,'home/update_pending.html',{
		'pending':pending,
		'form':form,
		})


def quick_search(request,rma,sn):
	
	rma = rma.upper()
	sn = sn.upper()
	pending = Pending.objects.get(rma_id=rma)
	parts = Part.objects.all()
	rcodes = Rcode.objects.all()
	rcount = rcodes.count()
	if sn==pending.rma_id.sn.upper():

		return render(request,'home/quick_search.html',{
			'pending':pending,
			'rma':rma,
			'sn':sn,
			'parts':parts,
			'rcodes':rcodes,

			})

def home(request):
	pendings=()
	nums=''
	user_login=()
	counts = 0
	events = Event.objects.all()
	parts = Part.objects.all()
	rcodes = Rcode.objects.all()
	rcount = rcodes.count()
	# home and device section
	try:
		user_login = User.objects.get(username=request.user)
		if user_login.is_ffvn:
			pendings = Pending.objects.all().order_by('rma_id__customer')
			
		elif user_login.dealer != None:
			pendings = Pending.objects.filter(dealer=user_login.dealer).order_by('rma_id__customer')

		elif user_login.customer != None:
			pendings = Pending.objects.filter(rma_id__customer=user_login.customer).order_by('-rma_id')

		counts = pendings.count()

		# set up pagination
		p = Paginator(pendings,10) #3 items /page
		page = request.GET.get('page')
		pendings = p.get_page(page)
		nums = 'a' * pendings.paginator.num_pages
	except:
		pass
 
	# return render(request,'themes/trial.html',{
	# 	'pendings':pendings,
	# 	'user_login':user_login,
	# 	'nums':nums,
	# 	'counts':counts,
	# 	})


	# quick search
	if request.method=="POST":
		rma = request.POST['rma']
		sn = request.POST['sn']
		rma = rma.upper()
		sn = sn.upper()
		try:
			pending = Pending.objects.get(rma_id=rma)
			if sn==pending.rma_id.sn.upper():
				return redirect(f'quick_search/{rma}/{sn}')
			else:
				messages.error(request,('Thông tin chưa chính xác 1.<br> Vui lòng liên hệ <a href="https://zalo.me/84902343992" target="_blank" rel="noopener noreferrer">Trần Minh Sang</a> để cập nhật thông tin thiết bị.'))
				return render(request,'home/home.html',{
					'pendings':pendings,
					'user_login':user_login,
					'nums':nums,
					'counts':counts,
					})
		except:
			messages.error(request,('Thông tin chưa chính xác 2.<br> Vui lòng liên hệ <a href="https://zalo.me/84902343992" target="_blank" rel="noopener noreferrer">Trần Minh Sang</a> để cập nhật thông tin thiết bị.'))
			return render(request,'home/home.html',{
							'pendings':pendings,
							'user_login':user_login,
							'nums':nums,
							'counts':counts,
							'events':events,
							
							})	
	# else:	



	return render(request,'home/home.html',{
			'pendings':pendings,
			'user_login':user_login,
			'nums':nums,
			'counts':counts,
			'events':events,
			
		})
