from django.shortcuts import render

# Create your views here.
from datetime import date, datetime
from pyexpat.errors import messages
from urllib import request
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def index(request):
    return render(request, 'index.html')

def admin_login(request):
    error=""
    if request.method=='POST':
        u=request.POST['uname']
        p=request.POST['pwd']
        user=authenticate(username=u,password=p)
        try:
            if user.is_staff:
                login(request,user)
                error="no"
            else:
                error="yes"
        except:
            error="yes"
    d={'error':error}
    return render(request,'admin_login.html',d)





from django.contrib.auth.models import User
from .models import Provider

def provider_signup(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        con = request.POST['contact']
        e = request.POST['email']
        gen = request.POST['gender']
        img = request.FILES['image']
        p = request.POST['pwd']
        try:
            if User.objects.filter(username=e).exists():
                # If email already exists, set error message
                error = "Email already exists"
            elif Provider.objects.filter(mobile=con).exists():
                # If contact number already exists, set error message
                error = "Contact number already exists"
            else:
                # Otherwise, create new user
                user = User.objects.create_user(first_name=f, last_name=l, username=e, password=p)
                # Create a new provider with an auto-generated id
                Provider.objects.create(user=user, mobile=con, image=img, gender=gen, type="provider", status="pending")
                error = "no"
        except Exception as e:
            print(e)
            error = "An error occurred"
    return render(request, 'provider_signup.html', {'error': error})

 
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def provider_login(request):
    error = ""
    success_message_provider = ""  # Initialize success message
    
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        
        if user:
            try:
                user1 = Provider.objects.get(user=user)
                
                if user1.type == "provider" and user1.status != "pending":
                    login(request, user)
                    error = "no"
                else:
                    error = "not"
            except Provider.DoesNotExist:
                error = "yes"
        else:
            error = "yes"
    
    # Retrieve success message from session data
    
    
    d = {'error': error}
    return render(request, 'provider_login.html', d)



def user_signup(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        con = request.POST['contact']
        e = request.POST['email']
        gen = request.POST['gender']
        img = request.FILES['image']
        p = request.POST['pwd']
        a = request.POST['address']
        try:
            if User.objects.filter(username=e).exists():
                # If email already exists, set error message
                error = "Email already exists"
            elif CustomerUser.objects.filter(mobile=con).exists():
                # If contact number already exists, set error message
                error = "Contact number already exists"
            else:
                # Otherwise, create new user
                user = User.objects.create_user(first_name=f, last_name=l, username=e, password=p)
                CustomerUser.objects.create(user=user, mobile=con, image=img, gender=gen, type="customer",address=a)
                error = "no"
        except Exception as e:
            print(e)
            error = "An error occurred"
    return render(request, 'user_signup.html', {'error': error})



def user_login(request):
    error=""
    if request.method == "POST":
        u=request.POST['uname']
        p=request.POST['pwd']
        user=authenticate(username=u,password=p)
        if user:
            try:
                user1=CustomerUser.objects.get(user=user)
                if user1.type == "customer":
                    login(request,user)
                    error="no"
                else:
                    error="yes"
            except:
                error="yes"
        else:
            error="yes"
    d={'error':error}
    return render(request,'user_login.html',d)


def user_home(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user = request.user
    data = CustomerUser.objects.get(user=user)
    error=""
    if request.method=='POST':
        f = request.POST['fname']
        l = request.POST['lname']
        con = request.POST['contact']
        e = request.POST ['email']
        a = request.POST ['address']
       
    

        data.user.first_name=f
        data.user.last_name=l
        data.user.username=e
        data.mobile=con
        data.address=a
        try:
            data.save()
            error = "no"
        except:
            error = "yes"
        try:
            i=request.FILES['image']
            data.image=i 
            data.save()
            error = "no"
        except:
            pass
    d={'error':error,'data':data}
    return render(request,'user_home.html',d)

from django.shortcuts import render, redirect, HttpResponse
from .models import Provider
def provider_home(request):
    if not request.user.is_authenticated:
        return redirect('provider_login')
    
    try:
        user_provider = Provider.objects.get(user=request.user)
    except Provider.DoesNotExist:
        return HttpResponse("You are not a registered provider.")
    
    error = ""
    success_message_key = f'success_message_provider_{user_provider.id}'
    success_message_provider = request.session.pop(success_message_key, None)
    
    if request.method == 'POST':
        f = request.POST.get('fname')
        l = request.POST.get('lname')
        con = request.POST.get('contact')
        e = request.POST.get('email')
        
        user_provider.user.first_name = f
        user_provider.user.last_name = l
        user_provider.user.username = e
        user_provider.mobile = con
        
        try:
            user_provider.user.save()
            user_provider.save()
            error = "no"
        except Exception as e:
            error = "yes"
        
        try:
            i = request.FILES.get('image')
            if i:
                user_provider.image = i 
                user_provider.save()
            error = "no"
        except Exception as e:
            pass
    
    context = {'error': error, 'data': user_provider, 'success_message_provider': success_message_provider}
    return render(request, 'provider_home.html', context)




def user_logout(request):
    logout(request)
    return redirect('index')

def provider_logout(request):
    logout(request)
    return redirect('index')

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    pcount = Provider.objects.all().count()
    scount = CustomerUser.objects.all().count()
    d={'pcount':pcount,'scount':scount}
    return render(request,'admin_home.html',d)

def admin_logout(request):
    logout(request)
    return redirect('index')

def view_users(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=CustomerUser.objects.all()
    d={'data':data}
    return render(request,'view_users.html',d)

def delete_user(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    customer=CustomerUser.objects.get(id=pid)
    customer.delete()
    return redirect('view_user')

def delete_provider(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    customer=Provider.objects.get(id=pid)
    customer.delete()
    return redirect('provider_all')

def provider_pending(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Provider.objects.filter(status='pending')
    d={'data':data}
    return render(request,'provider_pending.html',d)

def change_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    
    error = ""  # Define error variable with an initial value
    provider = Provider.objects.get(id=pid)
    
    if request.method=="POST":
        s = request.POST['status']
        provider.status = s
        try:
            provider.save()
            error = "no"
        except:
            error = "yes"
    
    d = {'provider': provider, 'error': error}
    return render(request, 'change_status.html', d)

def provider_accepted(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Provider.objects.filter(status='Accept')
    d={'data':data}
    return render(request,'provider_accepted.html',d)

def provider_rejected(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Provider.objects.filter(status='Reject')
    d={'data':data}
    return render(request,'provider_rejected.html',d)

def provider_all(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Provider.objects.all()
    d={'data':data}
    return render(request,'provider_all.html',d)


def delete_provider(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    provider=User.objects.get(id=pid)
    provider.delete()
    return redirect('provider_all')


def delete_user(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    customer=User.objects.get(id=pid)
    customer.delete()
    return redirect('view_users')

def admin_passwordchange(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    
    error = ""  # Define error variable with an initial value
    if request.method=="POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
       
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error="not"
        except:
            error = "yes"
    
    d = {'error': error}
    return render(request, 'admin_passwordchange.html',d)

def user_passwordchange(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    
    error = ""  # Define error variable with an initial value
    if request.method=="POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
       
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error="not"
        except:
            error = "yes"
    
    d = {'error': error}
    return render(request, 'user_passwordchange.html', d)

def provider_passwordchange(request):
    if not request.user.is_authenticated:
        return redirect('provider_login')
    
    error = ""  # Define error variable with an initial value
    if request.method=="POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
       
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error="not"
        except:
            error = "yes"
    
    d = {'error': error}
    return render(request, 'provider_passwordchange.html', d)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Service, Provider

def create_service(request):
    if not request.user.is_authenticated:
        return redirect('provider_login')  # Adjust 'provider_login' to your actual login URL
    
    error = ""
    detail = None
    
    if request.method == 'POST':
        try:
            s = request.POST.get('service_name')
            ex = request.POST.get('experience')
            l = request.POST.get('location')
            de = request.POST.get('description')
            
            # Check if a service with the same name exists for the current user
            if Service.objects.filter(service_name=s, provider__user=request.user).exists():
                error = "Duplicate"
                messages.warning(request, "You already have a service with the same name.")
            else:
                # Retrieve or create the Provider object associated with the current user
                provider = get_object_or_404(Provider, user=request.user)
                
                # Create the Service object
                detail = Service.objects.create(provider=provider, service_name=s,
                                                 experience=ex, location=l,
                                                 description=de)
                error = "no"
            
        except Exception as e:
            print(e)
            error = "yes"
            # Add a meaningful error message to be displayed to the user
            messages.error(request, "An error occurred while processing your request.")
    
    d = {'error': error, 'detail': detail}
    return render(request, 'create_service.html', d)


from django.shortcuts import get_object_or_404

def view_services(request):
    if not request.user.is_authenticated:
        return redirect('provider_login')
    try:
        user = request.user
        provider = Provider.objects.get(user=user)
        services = Service.objects.filter(provider=provider)
    except Provider.DoesNotExist:
        # Handle the case where the provider does not exist
        services = []

    context = {'services': services}
    return render(request, 'view_services.html', context)

def edit_service(request, pid):
    if not request.user.is_authenticated:
        return redirect('provider_login')
    
    error = ""
    service = Service.objects.get(id=pid)
    
    if request.method == 'POST':
        try:
            s = request.POST['service_name']
            ex = request.POST['experience']
            l = request.POST['location']
            de = request.POST['description']

            service.service_name = s
            service.experience = ex
            service.location = l
            service.description = de
            
            service.save()
            error = "no"
        except Exception as e:
            print(e)
            error = "yes"
    
    d = {'error': error, 'service': service}
    return render(request, 'edit_service.html', d)




def change_image(request,pid):
    if not request.user.is_authenticated:
        return redirect('provider_login')
    error=""
    service=Provider.objects.get(id=pid)
    if request.method == 'POST':
        im = request.POST['image']
        

        service.image=im
        
        try:
            service.save()
            error="no"
        except:
            error="yes "
    d={'error':error,'service':service}
    return render(request, 'change_image.html',d)




def service_list(request):
    data = Service.objects.all()
    d = {'data': data}
    return render(request, 'service_list.html', d)

from .models import Service

def manage_services(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin_login')
    
    try:
        services = Service.objects.all()
    except Service.DoesNotExist:
        services = []

    context = {'services': services}
    return render(request, 'manage_services.html', context)

def delete_service(request, service_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin_login')
    
    service = Service.objects.get(id=service_id)
     # Assuming the related name is 'provider_set'
    
    # Delete the service
    service.delete()
    return redirect('manage_services')

def delete_service1(request, service_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('provider_login')
    
    service = Service.objects.get(id=service_id)
     # Assuming the related name is 'provider_set'
    
    # Delete the service
    service.delete()
    return redirect('view_services')

def search_service(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    service = Service.objects.all()
    user = request.user
    try:
        customer = CustomerUser.objects.get(user=user)
        data = Orders.objects.filter(customer=customer)
        li = [i.service.id for i in data]
        d = {'service': service, 'li': li, 'data': data, 'customer': customer}
    except CustomerUser.DoesNotExist:
        # Handle the case where CustomerUser does not exist for the user
        # For example, you can redirect the user to a page indicating that they need to set up their customer profile.
        return redirect('search_service')
    return render(request, 'search_service.html', d)


def service_detail(request,pid):
    service = Service.objects.get(id=pid)
    d = {'service': service}
    return render(request, 'service_detail.html', d)


def apply_service(request, pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    
    error_msg = ""
    error = ""
    success_messages = {}  # Dictionary to store success messages for each provider
    user = request.user
    customer = CustomerUser.objects.get(user=user)
    
    try:
        service = Service.objects.get(id=pid)
        serviceman = service.provider
    except Service.DoesNotExist:
        error_msg = "Service does not exist."
        context = {'error': error_msg}
        return render(request, 'apply_service.html', context)
    
    if request.method == 'POST':
        da = request.POST.get('date')
        try:
            selected_date = datetime.strptime(da, '%Y-%m-%d').date()
            current_date = datetime.now().date()
            
            if selected_date < current_date:
                error_msg = "Please select a present or future date."
            else:
                try:
                    # Creating order with associated customer, service, and provider
                    Orders.objects.create(customer=customer, service=service, serviceman=serviceman, apply_date=selected_date, status="pending")
                    
                    error = "no"
                except Exception as e:
                    error_msg = "An error occurred while processing your request: " + str(e)
        except ValueError:
            error_msg = "Invalid date format. Please use YYYY-MM-DD format."

    context = {'error': error_msg, 'success_messages': success_messages, 'data': service,'error': error}
    return render(request, 'apply_service.html', context)








from .models import Orders

def request(request):
    if not request.user.is_authenticated:
        return redirect('provider_login')
    
    try:
        # Filter Orders queryset to include only orders associated with the current user
        serviceman = Provider.objects.get(user=request.user)
        service_requests = Orders.objects.filter(serviceman=serviceman,status='pending')
        d = {'service_requests': service_requests}
        return render(request, 'request.html', d)
    except Orders.DoesNotExist:
        # Handle the case where Orders do not exist for the user
        # For example, you can redirect the user to a page indicating that they have no pending orders.
        return redirect('request')


    
from .models import Orders

def request_all(request):
    if not request.user.is_authenticated:
        return redirect('provider_login')
    
    try:
        serviceman = Provider.objects.get(user=request.user)
        service_requests = Orders.objects.filter(serviceman=serviceman)
        d = {'service_requests': service_requests}
        return render(request, 'request_all.html', d)
    except Orders.DoesNotExist:
        # Handle the case where Orders do not exist for the user
        # For example, you can redirect the user to a page indicating that they have no orders.
        return redirect('request_all')
    

def request_accept(request):
    if not request.user.is_authenticated:
        return redirect('provider_login')
    
    try:
        serviceman = Provider.objects.get(user=request.user)
        service_requests = Orders.objects.filter(serviceman=serviceman,status='Accept')
        d = {'service_requests': service_requests}
        return render(request, 'request_accept.html', d)
    except Orders.DoesNotExist:
        # Handle the case where Orders do not exist for the user
        # For example, you can redirect the user to a page indicating that they have no orders.
        return redirect('request_accept')
    
def request_reject(request):
    if not request.user.is_authenticated:
        return redirect('provider_login')
    
    try:
        serviceman = Provider.objects.get(user=request.user)
        service_requests = Orders.objects.filter(serviceman=serviceman,status='Reject')
        d = {'service_requests': service_requests}
        return render(request, 'request_reject.html', d)
    except Orders.DoesNotExist:
        # Handle the case where Orders do not exist for the user
        # For example, you can redirect the user to a page indicating that they have no orders.
        return redirect('request_reject')



from django.shortcuts import render, redirect
from .models import Orders
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def changecustomer_status(request, pid):
    if not request.user.is_authenticated:
        return redirect('provider_login')
    
    error = ""  # Define error variable with an initial value
    order = Orders.objects.get(id=pid)
    
    if request.method == "POST":
        status = request.POST.get('status')
        order.status = status
        try:
            order.save()
            error = "no"
        
            
        except Exception as e:
            error = "An error occurred while processing your request: " + str(e)
    
    d = {'order': order, 'error': error}
    return render(request, 'changecustomer_status.html', d)




def my_request(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    
    try:
        customer = CustomerUser.objects.get(user=request.user)
        service_requests = Orders.objects.filter(customer=customer)
        return render(request, 'my_request.html', {'service_requests': service_requests})
    except CustomerUser.DoesNotExist:
        # Handle the case where CustomerUser does not exist for the user
        # For example, you can redirect the user to a page indicating that they need to set up their customer profile.
        return redirect('my_request')

def delete_request(request,pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    service=Orders.objects.get(id=pid)
    service.delete()
    return redirect('my_request')

def view_orders(request):
    data = Orders.objects.all()
    d = {'data': data}
    return render(request, 'view_orders.html', d)
