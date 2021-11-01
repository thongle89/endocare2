from django.shortcuts import render,redirect
from .models import Event,Comment
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()
# Create your views here.
def events(request):
	events = Event.objects.all()
	return render(request,'whiteboard/events.html',{
		'events':events,
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
	