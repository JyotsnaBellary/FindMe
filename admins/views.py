from vendor.models import *
from .models import *
from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password, check_password



# Create your views here.
from django.shortcuts import render

# Create your views here.
def adminpage(request):
    admin = request.session['admin']
    print('hi')
    if request.method == "POST":
        print("heel")
        if request.POST['Accept']:
            email = request.POST['email']
            print(email)
            contact_info.objects.filter(email = email).update(status='Accept')
            vendors_not_verified = contact_info.objects.filter(status = "NotVerified").all()        
            # print(i[0].status) 
            return render(request, 'adminpage.html', {'username': admin, 'Not_Verified': vendors_not_verified})   
    else:
        vendors_not_verified = contact_info.objects.filter(status = "NotVerified").all()        
        return render(request, 'adminpage.html', {'username': admin, 'Not_Verified': vendors_not_verified})

def adminlogin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        if email != "" and password != "":
            try:
                adminInfo = register.objects.get(email = email)
                flag = check_password(password, adminInfo.password)
                # pass1 = customerInfo.password
                # if pass1 == password:
                if flag:
                    request.session['admin'] = adminInfo.username
                    response = redirect('adminpage')
                    return response
                else:
                    error_str = "Error: Incorrect Password"
                    messages.error(request, error_str)
                    return render(request, 'adminlogin.html')
            except Exception:
                    messages.error(request, "You haven't been registered yet!")
                    return render(request, 'adminlogin.html')
        else:
            error_str = "Error: "
            
            if email == "":
                error_str = error_str + '-Empty Empty field! '
            if password == "":
                error_str = error_str + '-Empty Password field! '
            messages.error(request, error_str)
            return render(request, 'adminlogin.html')
    return render(request, 'adminlogin.html')
