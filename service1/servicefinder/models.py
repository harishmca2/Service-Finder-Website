from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class CustomerUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    mobile = models.CharField(max_length=15, null=True)
    image = models.FileField(null=True)
    gender = models.CharField(max_length=15, null=True)
    type = models.CharField(max_length=15, null=True)
    address=models.CharField(max_length=255, null=True)
    def _str_(self):
        return self.user.username

class Provider(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    mobile = models.CharField(max_length=15, null=True)
    image = models.FileField(null=True)
    gender = models.CharField(max_length=15, null=True)
    type = models.CharField(max_length=15, null=True)
    status = models.CharField(max_length=15, null=True)

    def _str_(self):
        return self.user.username

class Service(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, null=True)
    service_name = models.CharField(max_length=15, null=True)
    experience = models.CharField(max_length=15, null=True)
    location = models.CharField(max_length=150, null=True)
    description = models.CharField(max_length=200, null=True)

    def _str_(self):
        return self.service_name


class Orders(models.Model):
    customer = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    serviceman = models.ForeignKey(Provider, on_delete=models.CASCADE, null=True)
    apply_date = models.DateField(null=True)
    status = models.CharField(max_length=20, null=True)
    statu = models.CharField(max_length=20, null=True)

    def _str_(self):
        return self.serviceman
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) 