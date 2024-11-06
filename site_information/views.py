from django.shortcuts import render, redirect
from django.views import View
from .models import SiteInfo
from .forms import SiteInfoForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
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
            messages.success(request, "اطلاعات با موفقیت به روز شد.")
            return render(request, self.template_name, {'form': form, 'site_info': site_info})

        return render(request, self.template_name, {'form': form, 'site_info': site_info})
