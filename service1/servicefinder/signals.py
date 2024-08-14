# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Orders, Notification

@receiver(post_save, sender=Orders)
def notify_serviceman(sender, instance, created, **kwargs):
    if created:
        serviceman = instance.serviceman
        message = f"New service booked by {instance.customer.user.username}."
        Notification.objects.create(user=serviceman.user, message=message)
