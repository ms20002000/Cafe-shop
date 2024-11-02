from django.shortcuts import render, redirect
from .models import Order, OrderItem
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import OrderForm, OrderItemFormSet 
from django.http import JsonResponse
from django.conf import settings
import string
import random
from django.views import View
class OrderCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'order/create_order.html'
    success_url = reverse_lazy('staff_dashboard')

    def test_func(self):
        return self.request.user.is_staff
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['is_update'] = False  
        return kwargs

    def form_valid(self, form):
        order = form.save(commit=False)
        order.modify_by = self.request.user  
        order.save()

        formset = OrderItemFormSet(self.request.POST, instance=order)
        if formset.is_valid():
            formset.save()
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = OrderItemFormSet(self.request.POST)
        else:
            context['formset'] = OrderItemFormSet()
        return context


class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Order
    template_name = 'order/delete_order.html'
    success_url = reverse_lazy('staff_dashboard')

    def test_func(self):
        return self.request.user.is_staff

class OrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'order/update_order.html'
    success_url = reverse_lazy('staff_dashboard')

    def test_func(self):
        return self.request.user.is_staff
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['is_update'] = True  
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = OrderItemFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = OrderItemFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()  
            formset.instance = self.object
            formset.save()  
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)
        
from django.views import View
from django.http import JsonResponse
import string
import random
from django.conf import settings

class OrderSessionView(View):
    def generate_random_id(self, length=8):
        """Generate a random ID consisting of uppercase letters and digits."""
        characters = string.ascii_uppercase + string.digits
        random_id = ''.join(random.choice(characters) for _ in range(length))
        return random_id

    def get(self, request, *args, **kwargs):
        """Retrieve the order session."""
        order = request.session.get('cart')
        if order:
            return JsonResponse({'message': 'Order retrieved successfully', 'order': order}, status=200)
        else:
            return JsonResponse({'message': 'No order session found'}, status=404)

    def post(self, request, *args, **kwargs):
        """Add the cart from cookies to the session."""
        cart_items = request.COOKIES.get(settings.CART_COOKIE_NAME)

        if cart_items:
            order_details = {
                'order_id': self.generate_random_id(),
                'order_details': cart_items,
                'status': 'Created'
            }
            request.session['order'] = order_details
            return JsonResponse({'message': 'Cart saved to session', 'order': order_details}, status=200)
        else:
            return JsonResponse({'message': 'No cart items found in cookies'}, status=404)

    def delete(self, request, *args, **kwargs):
        """Delete the order session."""
        if 'order' in request.session:
            del request.session['order']
            return JsonResponse({'message': 'Order session deleted successfully'}, status=200)
        else:
            return JsonResponse({'message': 'No order session found'}, status=404)

    def put(self, request, *args, **kwargs):
        """Update the status of the order."""
        if 'order' in request.session:
            new_status = request.POST.get('status')
            if new_status:
                request.session['order']['status'] = new_status
                return JsonResponse({'message': 'Order status updated', 'order': request.session['order']}, status=200)
            else:
                return JsonResponse({'message': 'No status provided'}, status=400)
        else:
            return JsonResponse({'message': 'No order session found'}, status=404)
