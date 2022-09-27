from cgi import print_form
from django.shortcuts import render
from concurrent.futures.process import _python_exit
from unicodedata import name
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from django.contrib import auth, messages

from customers.models import register as cregister
from . import models
from .models import *
from django.core.mail import send_mail
import math, random
from django.http import HttpResponse

# Create your views here.
def notverified(request):
    email = request.session['username']
    return render(request, 'notverified.html', {'currentss_email':email})

def filepath(filename):
    old_filename = filename
    old_filename = old_filename.replace(" ", "_")
    timeNow=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename= "%s%s" % (timeNow, old_filename)
    return os.path.join('uploads/', filename)

def vendor(request):
    return render(request, 'vendor_main.html')

def order(request):
    email = request.session['username']
    return render(request, 'order.html',{'current_email':email})


def signup(request):
    if request.method=='POST':
        name=request.POST['name']
        business_name=request.POST['vendor_name']
        email=request.POST['email']
        phone=request.POST['phone']
        password=request.POST['password']
        #validation
        value = {
            'name':name,
            'business_name':business_name,
            'email':email,
            'phone':phone,
        }
        #creating and object which will be saved later down
        signup=register(name=name, business_name=business_name, email=email, phone_no=phone, password=password)
        if(len(phone)> 10 or len(phone)<10):
            messages.error(request, "Enter valid Phone number !")
            return render(request, "signup.html", {'values':value})

        elif(len(password) < 6):
            messages.error(request, "Password must be atleast 6 characters!")
            return render(request, "signup.html", {'values':value})

        #checking if the email already exists
        elif signup.isExists():
            messages.error(request, "Email Address Already Registered.hello.")
            return render(request, "signin.html", {'values':value})
        else:
            signup.password=make_password(signup.password)
            signup.save()
            profile=register.objects.get(email = email)
            # info = contact_info(Person_name = profile.name, email = profile.email, mobile_no = profile.phone_no, status = "NotVerified", vendor_id = profile.vendor_id)
            # info.save()
            request.session['username'] = email
            return redirect('bussiness_profile')           
    else:
        return render(request, "signup.html")

def signin(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        signin=register.get_vendor_by_email(email)
        if signin:
            try:
                profile = contact_info.objects.get(email = email)
            except Exception:
                return render(request, "bussiness_profile.html")

            flag=check_password(password, signin.password)   #returns true or false
            if flag:
                request.session['username'] = email
                if profile.status=="Accept":
                    response = redirect('vendor_profile')
                    return response
                elif profile.status == 'NotVerified':
                    response = redirect('notverified')
                    return response
                elif profile.status == 'Reject':
                    response = redirect('vendor_profile')
                    return response
            else:
                messages.error(request, "Email or Password invalid!")
                return render(request, "signin.html")
            
        else:
            messages.error(request, "Please Register!")
            return render(request, "signup.html")
    else:
        return render(request, "signin.html")
   


def vendor_profile(request):
    email = request.session['username']
    if request.method =='POST':
        if 'Edit_About' in request.POST:
            About = request.POST['Edit_About']
            print(About)
            contact_info.objects.filter(email=email).update(about=About)            
            vendor = contact_info.objects.get(email = email)
            print(vendor, 'helllo')
        elif 'name' in request.POST:
            print(request.POST['name'], 'rello')
            name=request.POST['name']
            desg=request.POST['designation']
            mobile_no=request.POST['mobile_no']
            alter_no=request.POST['alternate_no']
            About = request.POST['about']
            contact_info.objects.filter(email=email).update(Person_name = name, designaton = desg, mobile_no = mobile_no, alternate_no = alter_no, about = About)  
            vendor = contact_info.objects.get(email = email)
        elif 'company_name' in request.POST:
            print(request.POST['company_name'], 'rello')
            company_name = request.POST['company_name']
            year = request.POST['year']
            ceo = request.POST['ceo']
            address1 = request.POST['address1']
            address2 = request.POST['address2']
            pincode = request.POST['pincode']
            city = request.POST['city']
            state = request.POST['state']
            country = request.POST['country']
            landmark = request.POST['landmark']

            contact_info.objects.filter(email=email).update(company_name = company_name, ceo_name = ceo, year_established = year, address_line1 = address1, address_line2 = address2, pincode = pincode, city = city, state = state, country = country, landmark = landmark)  
            vendor = contact_info.objects.get(email = email)
            print(vendor.city, vendor.ceo_name,vendor.company_name ,vendor.state,'helllo')
            # return render(request, "vendor_profile.html", {'current_email':email, 'vendor':vendor})
    # else:
    vendor_id = register.objects.get(email = email).vendor_id
    products = add_product.objects.filter(vendor_id = vendor_id)
    orders = OrderProduct.objects.filter(vendor_id = vendor_id)
    for order in orders:
        order.product = add_product.objects.get(product_id = order.product_id)
        order.user = cregister.objects.get(user_id = order.user_id)
        order.order = Order.objects.get(order_id = order.order_id)
        # print(order.user.name, 'usert')
    vendor = contact_info.objects.get(email = email)
    context = {
        'products': products,
        'orders' : orders,
        'vendor':vendor,
        'current_email':email,
    }
    # print(vendor, 'helllo')
    return render(request, "vendor_profile.html", context)

    
def bussiness_profile(request):
    email = request.session['username']
    vendor = register.objects.get(email = email).vendor_id

    if request.method=='POST':
        name=request.POST['Person_name']
        emails=request.POST['emails']
        desg=request.POST['designation']
        mobile_no=request.POST['mobile_no']
        whatsapp_no=request.POST['whatsapp_no']
        company_name=request.POST['company_name']
        year=request.POST['year_established']
        # ceo=request.POST['ceo_name']
        website=request.POST['website']
        instagram=request.POST['Instagram']
        facebook=request.POST['Facebook']
        address1=request.POST['address_line1']
        address2=request.POST['address_line2']
        pincode=request.POST['pincode']
        city=request.POST['city']
        state=request.POST['state']
        country=request.POST['country']
        landmark=request.POST['landmark']
        if len(request.FILES)!=0:
            profile_image=request.FILES['photo']
            company_image=request.FILES['company_photo']
            if contact_info.objects.filter(vendor_id = vendor).exists():
                contact_info.objects.filter(vendor_id = vendor).delete()
                company_details = contact_info(vendor_id = vendor, Person_name=name, profile_pic=profile_image, email=emails,designaton=desg,mobile_no=mobile_no,whatsapp_no=whatsapp_no,company_name=company_name,company_logo=company_image,
                year_established = year,website=website,instagram = instagram, facebook = facebook, address_line1=address1,address_line2=address2,pincode=pincode,
                city=city,state=state,country=country,landmark=landmark)
                company_details.save()
            else:
                vendor = register.objects.get(email = email).vendor_id
                company_details=contact_info(vendor_id = vendor, Person_name=name, profile_pic=profile_image, email=emails,designaton=desg,mobile_no=mobile_no,whatsapp_no=whatsapp_no,company_name=company_name,company_logo=company_image,
                year_established = year,website=website,instagram = instagram, facebook = facebook, address_line1=address1,address_line2=address2,pincode=pincode,
                city=city,state=state,country=country,landmark=landmark)
                company_details.save()
        else:
            if contact_info.objects.get(vendor_id = vendor).exists():
                contact_info.objects.filter(vendor_id = vendor).update(Person_name=name, profile_pic=profile_image, email=emails,designaton=desg,mobile_no=mobile_no,whatsapp_no=whatsapp_no,company_name=company_name,company_logo=company_image,
                year_established = year,website=website,instagram = instagram, facebook = facebook, address_line1=address1,address_line2=address2,pincode=pincode,
                city=city,state=state,country=country,landmark=landmark)            
            else:
                messages.error(request, "Please select an image!!")
                return render(request, 'business_profile.html')
        vendor = contact_info.objects.get(email = email)

        context={
            'vendor':vendor,
        }
        
        if vendor.status == 'NotVerified':
            response = redirect('notverified')
        else:
            response = redirect('vendor_profile')
        return response
    else:
        vendor = register.objects.get(email = email)
        return render(request, "bussiness_profile.html", {'vendor':vendor})

    # vendor_id = vendor.objects.filter(email = email)
    # if request.method=='POST':
    #     name=request.POST['Person_name']
    #     emails=request.POST['emails']
    #     desg=request.POST['designation']
    #     mobile_no=request.POST['mobile_no']
    #     alter_no=request.POST['alternate_no']
    #     company_name=request.POST['company_name']
    #     year_established=request.POST['year_established']
    #     company_ceo=request.POST['ceo_name']
    #     website=request.POST['website']
    #     address_l1=request.POST['address_line1']
    #     address_l2=request.POST['address_line2']
    #     pincode=request.POST['pincode']
    #     city=request.POST['city']
    #     state=request.POST['state']
    #     country=request.POST['country']
    #     landmark=request.POST['landmark']
    #     if len(request.FILES)!=0:
    #         profile_image=request.FILES['photo']
    #         company_image=request.FILES['company_photo']

    #     
    #     if company_details.status == 'NotVerified':
    #         response = redirect('notverified')
    #     else:
    #         response = redirect('vendor_profile')
    #     return response
    # else:
    #     return render(request, "bussiness_profile.html")

def add_products(request):
    email = request.session['username'] 
    vendor_id = register.objects.get(email = email).vendor_id
    if request.method=='POST':
        if 'id' in request.POST:
            product_id = request.POST['id'] 
            product_name=request.POST['Product_Name']
            slug = slugify(product_name)
            desc=request.POST['Description']
            price=request.POST['Price']
            stock  = request.POST['stock']
            if len(request.FILES)!=0:
                product_image=request.FILES['product_photo']
                # product_images=request.getlist['product_photos']
                add_product.objects.filter(product_id = product_id).delete()  
                product = add_product(product_id = product_id, vendor_id = vendor_id,product_image = product_image,slug = slug, product_name = product_name, Description = desc, Price = price, stock = stock)
                product.save()
            else:
                add_product.objects.filter(product_id = product_id).update(vendor_id = vendor_id,slug = slug, product_name = product_name, Description = desc, Price = price, stock = stock)         
        else:
            product_name=request.POST['Product_Name']
            desc=request.POST['Description']
            price=request.POST['Price']
            stock  = request.POST['stock']
            if len(request.FILES)!=0:
                product_image=request.FILES['product_photo']
                # product_images=request.getlist['product_photos']
            slug = slugify(product_name)
            vendor_id = register.objects.get(email=email).vendor_id
            product = add_product(vendor_id = vendor_id,product_image = product_image,slug = slug, product_name = product_name, Description = desc, Price = price, stock = stock)
            product.save()
        response = redirect('vendor_profile')
        return response
    else:
        if 'id' in request.GET:
            print(request.GET['id'], 'idss')
            vendor_id = register.objects.get(email = email).vendor_id
            product = add_product.objects.get(vendor_id = vendor_id, product_id = request.GET['id'])
            context = {
                'product': product,    
            }
            return render(request, "add_products.html", context)
        return render(request, "add_products.html")

    
def change_status(request, status, order_id, product_id):
    if status == 'Accept':
        OrderProduct.objects.filter(order_id = order_id, product_id = product_id, status = 'Placed').update(status = 'Accepted')
    elif status == 'Complete':
        OrderProduct.objects.filter(order_id = order_id, product_id = product_id, status = 'Accepted').update(status = 'Completed')

    return redirect('vendor_profile')

def delete_products(request, product):
    email = request.session['username'] 
    product_id = product
    add_product.objects.filter(product_id = product_id).delete()  
    if len(OrderProduct.objects.filter(product_id = product_id)) == 1:
        Order.objects.filter(order_id = OrderProduct.objects.filter(product_id = product_id).order_id).delete()
    OrderProduct.objects.filter(product_id = product_id).update(status = 'Cancelled')
    print(product_id)
    return redirect('vendor_profile')

def logout(request): 
    try:
        del request.session['username']
        return render(request, 'signin.html', {'message':'You have been successfully logged out!'})
    except Exception:
        return redirect('signin')