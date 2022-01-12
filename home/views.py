from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Pending,Part,Rcode,Device,Exfm
from .forms import PendingForm,CommentForm
from django.core.paginator import Paginator
#import User table from member
from django.contrib.auth import get_user_model
from django.http import HttpResponse
import xlwt
import datetime
from django.utils import timezone
User = get_user_model()
from django.db.models import Q

from whiteboard.models import Event,Comment,Media

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
			customer_name = user_login.customer.exfm_name

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
	

	for device in devices:
		row_num+=1

		for col_num in range(len(device)):
			if str(device[col_num]) != 'None':
				ws.write(row_num,col_num,str(device[col_num]),font_style)
	wb.save(response)
	
	return response

	
	
def comments(request,rma_id):
	comments = Comment.objects.all().order_by('cmt_time')
	
	if request.method=="POST":
		user_login = request.user
		cmt_text = request.POST['cmt_text']
		c = Comment.objects.create(rma_id = Exfm.objects.get(pk=rma_id),username=user_login,cmt_text=cmt_text)
		c.save()
		pending = Pending.objects.get(rma_id=rma_id)
		sn = pending.rma_id.sn
		messages.success(request,('Cập nhật thành công.'))
		return redirect('quick-search',rma_id,sn)
	else:
		return render(request,'home/comments.html',{
			'comments':comments,
			'rma':rma_id,
			# 'form':form,
			})
	

def update_pending(request,rma_id):
	pending = Pending.objects.get(rma_id=rma_id)
	parts = Part.objects.filter(rma=rma_id)
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
		'parts':parts,
		})

def parts_order(request,serial):
	rma = Exfm.objects.get(sn=serial.upper())
	pending = Pending.objects.get(rma_id=rma)
	parts = Part.objects.filter(rma=rma)
	# form = PartsOrderForm(request.POST or None,instance=pending)
	# instance: lấy mẫu cũ\
	# rma = pending.rma_id
	sn = serial # pending.rma_id.sn
	# if form.is_valid():
	# 	form.save()
		
	# 	messages.success(request,('Cập nhật thành công.'))
	# 	return redirect('parts-order',sn)
	# else:
	# 	return redirect('quick-search',rma,sn)
	return render(request,'home/parts_order.html',{
		'pending':pending,
		# 'form':form,
		'parts':parts,
		})
def quick_search(request,rma,sn):
	
	rma = rma.upper().strip()
	sn = sn.upper().strip()
	pending = Pending.objects.get(rma_id=rma)
	comments = Comment.objects.all().order_by('cmt_time')
	parts = Part.objects.all()
	rcodes = Rcode.objects.all()
	try:
		user_login = User.objects.get(username=request.user)
	except:
		user_login=''

	if sn==pending.rma_id.sn.upper():

		return render(request,'home/quick_search.html',{
			'pending':pending,
			'rma':rma,
			'sn':sn,
			'parts':parts,
			'rcodes':rcodes,
			'comments':comments,
			'user_login':user_login,

			})

def count_pending(pendings,count_score):
	count_p=0
	count_e=0
	count_count=0
	
	count_p = pendings.filter(p_score=count_score,rma_id__e_score__lt=count_score).count()
	count_e = pendings.filter(p_score__lt=count_score,rma_id__e_score=count_score).count()
	count_count = pendings.filter(p_score=count_score,rma_id__e_score=count_score).count()
	return count_count + count_p +count_e

def home(request):
	pendings=()
	nums=''
	user_login=()
	counts = 0
	events = Event.objects.filter(type_e=2,event_date__gte=timezone.now()).order_by('event_date')
	parts = Part.objects.all()
	rcodes = Rcode.objects.all()
	rcount = rcodes.count()
	nhan_hang=0
	kiem_tra=0
	chuan_bi_bao_gia=0
	cho_duyet_bh=0
	cho_xac_nhan=0
	cho_xac_nhan_3th=0
	chuan_bi_lk=0
	cho_sua_chua=0
	dang_sua_chua=0
	dang_giao_hang=0
	hoan_tat_giao_hang=0
	tra_hang=0
	mes_loc = False
	#Media import
	try:
		medias = Media.objects.all()[0]
	except:
		
		medias=[]

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
		# nhan_hang_p =pendings.filter(Q(p_score=0) | Q(rma_id__e_score=0)).count()
		nhan_hang =count_pending(pendings,0)
		kiem_tra = count_pending(pendings,1)
		
		chuan_bi_bao_gia = count_pending(pendings,2)
		# cho_duyet_bh = count_pending(pendings,)
		cho_xac_nhan = count_pending(pendings,3)
		chuan_bi_lk = count_pending(pendings,4)
		cho_sua_chua =count_pending(pendings,5)
		dang_sua_chua = count_pending(pendings,6)
		dang_giao_hang = count_pending(pendings,7)
		hoan_tat_giao_hang =count_pending(pendings,8)
		cho_xac_nhan_3th = count_pending(pendings,9)
		tra_hang =count_pending(pendings,10)
		# set up pagination
		p = Paginator(pendings,10) #3 items /page
		page = request.GET.get('page')
		pendings = p.get_page(page)
		nums = 'a' * pendings.paginator.num_pages
	except:
		pass

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
				messages.error(request,('Thông tin chưa chính xác.<br> Vui lòng liên hệ <a href="https://zalo.me/84902343992" target="_blank" rel="noopener noreferrer">Trần Minh Sang</a> để cập nhật thông tin thiết bị.'))
				return render(request,'home/home.html',{
					'pendings':pendings,
					'user_login':user_login,
					'nums':nums,
					'counts':counts,
					'medias':medias,
					})
		except:
			mes_loc = True
			messages.error(request,('Thông tin chưa chính xác.<br> Vui lòng liên hệ <a href="https://zalo.me/84902343992" target="_blank" rel="noopener noreferrer">Trần Minh Sang</a> để cập nhật thông tin thiết bị.'))
			comments = Comment.objects.all().order_by('cmt_time')
			# user_login=''
			rma=''
			sn=''
			return render(request,'home/quick_search.html',{
							# 'pending':pending,
							# 'rma':rma,
							# 'sn':sn,
							# 'parts':parts,
							# 'rcodes':rcodes,
							# 'comments':comments,
							# 'user_login':user_login,
							'mes_loc':mes_loc,
							})
			mes_loc = False
	# else:	



	return render(request,'home/home.html',{
			'pendings':pendings,
			'nhan_hang':nhan_hang,
			'kiem_tra':kiem_tra,
			'chuan_bi_bao_gia':chuan_bi_bao_gia,
			'cho_duyet_bh':cho_duyet_bh,
			'cho_xac_nhan':cho_xac_nhan,
			'cho_xac_nhan_3th':cho_xac_nhan_3th,
			'chuan_bi_lk':chuan_bi_lk,
			'cho_sua_chua':cho_sua_chua,
			'dang_sua_chua':dang_sua_chua,
			'dang_giao_hang':dang_giao_hang,
			'hoan_tat_giao_hang':hoan_tat_giao_hang,
			'tra_hang':tra_hang,
			'user_login':user_login,
			'nums':nums,
			'counts':counts,
			'events':events,
			'medias':medias,
			
		})
