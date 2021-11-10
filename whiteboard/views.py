from django.shortcuts import render,redirect
from .models import Event,Comment
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib import messages
from .forms import VerifyUserForm,EventForm
from django.http import HttpResponseRedirect, HttpResponse
User = get_user_model()
from django.core.mail import send_mail


# Create your views here.
def events(request):
	events = Event.objects.all()
	now=timezone.now()
	training_soon = events.filter(type_e=2,event_date__gte=now)
	pm_soon = events.filter(type_e=1,event_date__gte=now)
	event_pass = events.filter(event_date__lte=now)
	return render(request,'whiteboard/events.html',{
		
		'now':now,
		'training_soon':training_soon,
		'pm_soon':pm_soon,
		'event_pass':event_pass,
		})

def verify_comment(request,comment_id):
	comment = Comment.objects.filter(pk=comment_id)
	user_login = str(User.objects.get(username=request.user))
	comment.update(is_verified=True,verifier=user_login,verify_time=timezone.now()) 
	return redirect('feed-back')

def feed_back(request):
	comments = Comment.objects.all().order_by('cmt_time')
	return render(request,'whiteboard/feed_back.html',{
		'comments':comments
		})



def new_members(request):
	unverified = User.objects.all().order_by('-date_joined')
	return render(request,'whiteboard/new_members.html',{
		'unverified':unverified,
		})

def update_member(request,member_id):
	member = User.objects.get(pk=member_id)
	form = VerifyUserForm(request.POST or None,instance=member)
	title='Xác nhận thành viên'

	# instance: lấy mẫu cũ
	v_check=[member.is_ffvn,member.dealer,member.customer]
 
	if form.is_valid():
		if member.is_ffvn: cap_do = "FFVN"
		if member.dealer !='': cap_do = f"Đại lý-{member.dealer}"
		if member.customer !='': cap_do = f"Đơn vị sử dụng-{member.customer}"
		if member.customer.web_name !='': cap_do = f"Đơn vị sử dụng-{member.customer.web_name}"
		
		form.save()
		v_change=[member.is_ffvn,member.dealer,member.customer]
		if v_check != v_change:
			contents = f"""(Đây là email trả lời tự động. Vui lòng không phản hồi lại email này)

Kính gửi Quý khách {member.full_name},

Chúc mừng Quý khách đã tạo tài khoản thành công.

Tài khoản {member} của Quý khách đã được phân quyền ở cấp độ: {cap_do}

Xin chúc Qúy khách có một trải nghiệm hài lòng và thu được nhiều giá trị từ trang web FFVN Endo Care của chúng tôi.

Trân trong,
Thay mặt Trung Tâm Dịch vụ FUJIFILM Việt Nam
			"""
			try:
				messages.success(request,(f'Xác nhận thành công. Đã gửi email xác nhận đến {member.email}'))
				send_mail(
						'Xác nhận đăng ký thành công',
						contents,
						'noreply.endocare@gmail.com',
						[member.email],
					fail_silently=False,
				)
			except:
				messages.error(request,(f'Không thể gửi email đến {member.email}.<a href="https://accounts.google.com/DisplayUnlockCaptcha">DisplayUnlockCapcha</a>s'))
		return redirect('new-members')

	return render(request,'whiteboard/form_update.html',{
		'member':member,
		'form':form,
		'title':title,
		'v_check':v_check,
		})
def update_event(request,event_id):
	events = Event.objects.get(pk=event_id)
	form = EventForm(request.POST or None,instance=events)
	title = 'Cập nhật sự kiện'
	# instance: lấy mẫu cũ
	if form.is_valid():
		form.save()
		messages.success(request,('Cập nhật thành công.'))
		return redirect('events')

	return render(request,'whiteboard/form_update.html',{
		'events':events,
		'form':form,
		'title':title,
		})

def add_event(request):
	submitted = False
	if request.method == "POST":
		form = EventForm(request.POST)
		if form.is_valid():
			form.save()
			# return HttpResponseRedirect('?submitted=True')
			messages.success(request,('Tạo sự kiện thành công.'))
			return redirect('events')
	else:
		form = EventForm
		if 'submitted' in request.GET:
			submitted = True
	return render(request,'whiteboard/add_event.html',{
		'form':form,
		'submitted':submitted,
		})