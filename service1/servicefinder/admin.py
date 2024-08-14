from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(CustomerUser)
admin.site.register(Provider)
admin.site.register(Service)
admin.site.register(Orders)