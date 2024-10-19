from django.shortcuts import render, redirect
from .models import Cart, Order, CartItem
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class OrderCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Order
    fields = ['customer', 'product', 'status', 'quantity']
    template_name = 'staff/order_form.html'
    success_url = reverse_lazy('staff_dashboard')

    def test_func(self):
        return self.request.user.is_staff

class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Order
    template_name = 'staff/order_confirm_delete.html'
    success_url = reverse_lazy('staff_dashboard')

    def test_func(self):
        return self.request.user.is_staff

class OrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Order
    fields = ['status']
    template_name = 'staff/order_update_form.html'
    success_url = reverse_lazy('staff_dashboard')

    def test_func(self):
        return self.request.user.is_staff
