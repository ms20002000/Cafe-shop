from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import OrderItem, Order
from django.core.mail import send_mail
from django.conf import settings
from account.models import CustomUser

@receiver(post_save, sender=OrderItem)
@receiver(post_delete, sender=OrderItem)  
def update_order_total_price(sender, instance, **kwargs):
    order = instance.order
    order.total_price = order.total_price_amount()  
    order.save(update_fields=['total_price'])  


@receiver(post_save, sender=Order)
def send_order_notification_to_managers(sender, instance, created, **kwargs):
    if created:  
        managers = CustomUser.objects.filter(is_admin=True)
        manager_emails = [manager.email for manager in managers if manager.email]
        print(manager_emails)

        if manager_emails:
            send_mail(
                    subject='New Order Created',
                    message=f"A new order has been placed. Order ID: {instance.id}\n"
                            f"Total Amount: {instance.total_price}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=manager_emails,
                    fail_silently=False,
                )