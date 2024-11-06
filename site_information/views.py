from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import SiteInfo
from .forms import SiteInfoForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

class SiteInfoView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'site_information/update_site_information.html'

    def test_func(self):
        return self.request.user.is_admin

    def get(self, request):
        site_info = SiteInfo.objects.first()
        form = SiteInfoForm(instance=site_info)
        return render(request, self.template_name, {'form': form, 'site_info': site_info})

    def post(self, request):
        site_info = SiteInfo.objects.first()
        form = SiteInfoForm(request.POST, request.FILES, instance=site_info)

        if form.is_valid():
            form.save()
            return redirect('home') 

        return render(request, self.template_name, {'form': form, 'site_info': site_info})
