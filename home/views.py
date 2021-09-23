from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Pending
from .forms import PendingForm
from django.core.paginator import Paginator
#import User table from member
from django.contrib.auth import get_user_model

User = get_user_model()

from whiteboard.models import Event

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
	if sn==pending.rma_id.sn.upper():

		return render(request,'home/quick_search.html',{
			'pending':pending,
			'rma':rma,
			'sn':sn,

			})

def home(request):
	pendings=()
	nums=''
	user_login=()
	counts = 0
	events = Event.objects.all()
	# home and device section
	try:
		user_login = User.objects.get(username=request.user)
		if user_login.is_ffvn:
			pendings = Pending.objects.all().order_by('customer')
			
		elif user_login.dealer != None:
			pendings = Pending.objects.filter(dealer=user_login.dealer).order_by('customer')

		elif user_login.customer != None:
			pendings = Pending.objects.filter(customer=user_login.customer).order_by('-receive_date',)

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
				messages.error(request,('Thông tin chưa chính xác 1.<br> Vui lòng liên hệ <a href="https://zalo.me/84902343992">Trần Minh Sang</a> để cập nhật thông tin thiết bị.'))
				return render(request,'home/home.html',{
					'pendings':pendings,
					'user_login':user_login,
					'nums':nums,
					'counts':counts,
					})
		except:
			messages.error(request,('Thông tin chưa chính xác 2.<br> Vui lòng liên hệ <a href="https://zalo.me/84902343992">Trần Minh Sang</a> để cập nhật thông tin thiết bị.'))
			return render(request,'home/home.html',{
							'pendings':pendings,
							'user_login':user_login,
							'nums':nums,
							'counts':counts,
							})	
	else:	


		return render(request,'home/home.html',{
				'pendings':pendings,
				'user_login':user_login,
				'nums':nums,
				'counts':counts,
				'events':events,
				})
	