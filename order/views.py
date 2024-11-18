from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, Table
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import OrderForm, OrderItemFormSet, TableForm , UpdateOrderItemFormSet
from django.views import View
from django.conf import settings
from django.contrib import messages

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

        formset = OrderItemFormSet(self.request.POST, instance=order)
        if formset.is_valid():
            if False not in [item_form.get('DELETE') for item_form in formset.cleaned_data]:
                form.add_error(None, "You must add at least one order item.")
                return self.form_invalid(form)
            order.save()
            formset.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = OrderItemFormSet(self.request.POST)
        else:
            context['formset']= OrderItemFormSet() 
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
            context['formset'] = UpdateOrderItemFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = UpdateOrderItemFormSet(instance=self.object)
        
        context['total_price'] = self.object.total_price_amount()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()  
            formset.instance = self.object
            formset.save()  
            messages.success(self.request, "سفارش با موفقیت آپدیت شد.")
        else:
            messages.error(self.request, "خطایی در ذخیره سفارش رخ داد.")
            return self.render_to_response(context)
        return self.render_to_response(self.get_context_data())

    def form_invalid(self, form):
        messages.error(self.request, "خطایی در فرم سفارش رخ داد. لطفاً اطلاعات را بررسی کنید.")
        return self.render_to_response(self.get_context_data())


class TableListView(LoginRequiredMixin, UserPassesTestMixin,View):
    template_name = 'order/table_list.html'

    def test_func(self):
        return self.request.user.is_admin

    def get(self, request):
        tables = Table.objects.all()       
        return render(request, self.template_name, {'tables': tables, 'MEDIA_URL': settings.MEDIA_URL,})


class TableCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'order/table_form.html'

    def test_func(self):
        return self.request.user.is_admin

    def get(self, request):
        form = TableForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = TableForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "میز با موفقیت ایجاد شد.")
            return redirect('table_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
        return render(request, self.template_name, {'form': form})


class TableUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'order/table_form.html'

    def test_func(self):
        return self.request.user.is_admin

    def get(self, request, pk):
        table = get_object_or_404(Table, pk=pk)
        form = TableForm(instance=table)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        table = get_object_or_404(Table, pk=pk)
        form = TableForm(request.POST, request.FILES, instance=table)
        if form.is_valid():
            form.save()
            messages.success(request, "میز با موفقیت به‌روزرسانی شد.")
            return redirect('table_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
        return render(request, self.template_name, {'form': form})