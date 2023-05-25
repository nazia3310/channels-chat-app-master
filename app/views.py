from django.dispatch import receiver
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from app.models import Message
from django.db.models import Q
# Create your views here.

class Home(View):
    def get(self, request):
        return render(request, 'home.html')

class Login(View):
    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return redirect("login")

class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')
        
    def post(self, request):
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        re_password = request.POST.get("re-password")
        if password==re_password:
            user = User()
            user.first_name = fname
            user.last_name = lname
            user.username = username
            user.email = email
            user.set_password(password)
            user.save()
            login(request, User.objects.get(username=username))
            return redirect("dashboard")
        else:
            return redirect('signup')

class Dashboard(View):
    def get(self, request, username=None):
        if request.user.is_authenticated:
            content = {
                'me': User.objects.get(username=request.user.username), 
                'users': User.objects.filter(is_superuser=False).exclude(username=request.user.username)
            }
            if username != None:
                content['receiver'] = User.objects.get(username=username)
                content['chats'] = Message.objects.filter(Q(Q(sender__username=request.user.username) & Q(receiver__username=username)) | Q(Q(sender__username=username) & Q(receiver__username=request.user.username))).order_by('id')
                return render(request, 'chat.html', content)
            else:
                return render(request, 'dashboard.html', content)
        else:
            return redirect("login")
    
def logout_view(request):
    logout(request)
    return redirect("login")