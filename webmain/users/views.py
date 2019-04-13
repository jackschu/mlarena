from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate, logout

from .forms import LoginForm
# Create your views here.
def my_login(request):
    if request.method == "POST":
        username= request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in ')
            return HttpResponseRedirect(reverse('login'))
        else:
            messages.add_message(request, messages.ERROR, 'No account associated with this email ')
        return HttpResponse('would redirect to register')
            #          return HttpResponseRedirect(reverse('users:register'))
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form' : form})
    
