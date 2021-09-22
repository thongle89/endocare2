from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .forms import RegisterUserForm




def login_user(request):
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request,("Đăng nhập thành công.<br>Phiên đăng nhập có hiệu lực trong thời gian 60 phút. Quá thời gian này vui lòng đăng nhập lại."))
            return redirect('home')
            
        else:
            messages.error(request,('Username và Password không khớp...<br><a href="https://zalo.me/84847078741">Liên hệ.</a>'))
            return redirect('login-user')

    else:
        return render(request,'accounts/login.html')

def logout_user(request):
	logout(request)
	messages.info(request,("Đăng xuất thành công."))
	return redirect('home')

def register_user(request):
    if request.method =="POST":
        # form = UserCreationForm(request.POST)
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request, user)
            messages.success(request,("Registration Successful!"))
            return redirect('home')
        # else:
        #     message = request.GET.get('message')
        #     messages.error(request,(message))
        #     return redirect('register-user')


    else:
        # form=UserCreationForm()
        form=RegisterUserForm()
        


    return render(request,'accounts/register_user.html',{
        'form':form,
        })
            