from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as dj_logout
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView
from .models import RegularUser
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django import forms


class RegularUserCreateView(CreateView):
    model = RegularUser
    fields = ['email', 'first_name', 'last_name', 'phone_number', 'password']
    template_name = 'account/register.html'
    success_url = reverse_lazy('list_user') 

    def get_form_class(self):
        form_class = super().get_form_class()
        form_class.base_fields['password'].widget = forms.PasswordInput()  
        return form_class

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password']) 
        user.save()
        return super().form_valid(form)

@method_decorator(login_required(login_url='login'), name='dispatch')
class RegularUserListView(ListView):
    model = RegularUser
    template_name = 'account/list_users.html'


class UserLoginView(LoginView):
    template_name = 'account/login.html'
    success_url = reverse_lazy('list_user')

    def get_success_url(self):
        return self.success_url


def logout(request):
    if request.method == 'POST':
        dj_logout(request)
        return HttpResponseRedirect(reverse_lazy('register'))
    
    return render(request, 'account/logout.html', {})