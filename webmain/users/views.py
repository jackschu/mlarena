from django.views import generic
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from .models import CustomUser
from django.urls import reverse, reverse_lazy
from .forms import LoginForm, CustomUserCreationForm
# Create your views here.
def my_login(request):
    if request.method == "POST":

        username= request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in ')
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.add_message(request, messages.ERROR, 'No account associated with this email ')
        return HttpResponseRedirect(reverse('users:login'))

    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form' : form})
    
class Register(generic.CreateView):
    form_class = CustomUserCreationForm
    model = CustomUser
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'


def my_logout(request):
    print('hi')
    logout(request)
    return HttpResponseRedirect(reverse('index'))
