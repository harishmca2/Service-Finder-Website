"""
URL configuration for service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf import settings
from servicefinder.views import *
from django.conf.urls.static import static 

urlpatterns = [
    path('',index, name= 'index'),
   
    path('admin_login/',admin_login, name='admin_login'),
    path('provider_login/',provider_login, name='provider_login'),
    path('provider_signup/',provider_signup, name='provider_signup'),
    path('user_login/',user_login, name='user_login'),
    path('user_signup/',user_signup, name='user_signup'),
    path('user_home/',user_home, name='user_home'),
    path('user_logout/',user_logout, name='user_logout'),
    path('admin_home/',admin_home, name='admin_home'),
    path('admin_logout/',admin_logout, name='admin_logout'),
    path('view_users/',view_users, name='view_users'),
    path('provider_pending/',provider_pending, name='provider_pending'),
    path('provider_home/',provider_home, name='provider_home'),
    path('delete_user/<int:pid>',delete_user, name='delete_user'),
    path('change_status/<int:pid>',change_status, name='change_status'),
    path('provider_accepted/',provider_accepted, name='provider_accepted'),
    path('provider_rejected/',provider_rejected, name='provider_rejected'),
    path('provider_all/',provider_all, name='provider_all'),
    path('delete_provider/<int:pid>',delete_provider, name='delete_provider'),
    path('delete_user/<int:pid>',delete_user, name='delete_user'),
    path('admin_passwordchange',admin_passwordchange, name='admin_passwordchange'),
    path('user_passwordchange',user_passwordchange, name='user_passwordchange'),
    path('provider_passwordchange',provider_passwordchange, name='provider_passwordchange'),
    path('provider_logout/',provider_logout, name='provider_logout'),
    path('create_service',create_service, name='create_service'),
    path('service_list/',service_list, name='service_list'),
    path('view_services/',view_services, name='view_services'),
    path('manage_services/',manage_services, name='manage_services'),
    path('delete_service/<int:service_id>/',delete_service, name='delete_service'),
    path('delete_service1/<int:service_id>/',delete_service1, name='delete_service1'),
    path('edit_service/<int:pid>',edit_service, name='edit_service'),
    path('change_image/<int:pid>',change_image, name='change_image'),
    path('service_detail/<int:pid>',service_detail, name='service_detail'),
    path('apply_service/<int:pid>',apply_service, name='apply_service'),
    path('changecustomer_status/<int:pid>',changecustomer_status, name='changecustomer_status'),
    path('my_request/',my_request, name='my_request'),
    path('delete_request/<int:pid>',delete_request, name='delete_request'),
    path('view_orders/',view_orders, name='view_orders'),
    path('request/',request, name='request'),
    path('request_all/',request_all, name='request_all'),
    path('request_accept/',request_accept, name='request_accept'),
    path('request_reject/',request_reject, name='request_reject'),
    path('search_service/', search_service, name='search_service'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
