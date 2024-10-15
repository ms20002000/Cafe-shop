from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import UserRegistrationForm
from django.contrib.auth.models import User


from django.views.generic import CreateView, ListView
from .models import RegularUser
from django.urls import reverse_lazy

class RegularUserCreateView(CreateView):
    model = RegularUser
    fields = ['email', 'first_name', 'last_name', 'phone_number', 'royalty_points', 'password']
    template_name = 'account/register.html'
    success_url = reverse_lazy('list_user') 

class RegularUserListView(ListView):
    model = RegularUser
    template_name = 'account/list_users.html'



def register(request):
    if request.method == 'GET':
        form = UserRegistrationForm(request.POST)
        return render(request, 'account/register.html', {'form': form})
    elif request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            dj_login(request, user)
            # return render(request, 'account/dashboard.html', {'user': user})
            return render(request, 'account/list_users.html', {'users': User.objects.all()})
        else:
            return render(request, 'account/register.html', {'form': form})
    else:
        return HttpResponse('Only get/post method allowed')


def login_first(request):
    return HttpResponse('Please login first')


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            dj_login(request, user)
            return render(request, 'account/list_users.html', {'users': User.objects.all()})
        return HttpResponse('Wrong password/username')

    elif request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'account/login.html', {'form': form})

    return HttpResponse('Please login with post method')


# def login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             return render(request, 'account/dashboard.html', {'user': user})
#     else:
#         form = LoginForm()
#     return render(request, 'account/login.html', {'form': form})
    

@login_required(login_url='/account/login_first/')
def logout(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponse('Please login first')

        dj_logout(request)
        return HttpResponse('Logout successfully')

    return HttpResponse('Only post method allowed')

@login_required(login_url='/account/login_first/')
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})