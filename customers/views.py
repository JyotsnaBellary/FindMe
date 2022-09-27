from pickle import TRUE
import re
from tkinter import E
from django.shortcuts import get_object_or_404, render, redirect
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import auth, messages
import vendor.models
from vendor.models import Order
from .models import *
from django.http import HttpResponse
from .forms import *
# from vendor.views import *
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from vendor.forms import ReviewForm
# Create your views here.
def home(request):
    return render(request, 'home.html')


def activate(request):
    return 

# def Register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             phone_number = form.cleaned_data['phone_number']
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             username = email.split("@")[0]
#             user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
#             user.phone_number = phone_number
#             user.save()

#             # Create a user profile
#             profile = UserProfile()
#             profile.user_id = user.id
#             profile.profile_picture = 'default/default-user.png'
#             profile.save()

#             # USER ACTIVATION
#             current_site = get_current_site(request)
#             mail_subject = 'Please activate your account'
#             message = render_to_string('accounts/account_verification_email.html', {
#                 'user': user,
#                 'domain': current_site,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': default_token_generator.make_token(user),
#             })
#             to_email = email
#             send_email = EmailMessage(mail_subject, message, to=[to_email])
#             send_email.send()
#             # messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email address [rathan.kumar@gmail.com]. Please verify it.')
#             return redirect('/accounts/login/?command=verification&email='+email)
#     else:
#         form = RegistrationForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'Register.html', context)


def Register(request):
    if request.method == "POST":
        name = request.POST['Name']
        email = request.POST['Email']
        password = request.POST['Password']
        re_password = request.POST['RePassword']
        if name != "" and email != "" and password != "" and re_password != "":
            username = email.split("@")[0]
            if password == re_password:
                try:
                    password = make_password(password)
                    saveprofile = register(username = username, name = name,email = email, password = password) 
                    saveprofile.save()
                    return render(request, 'login.html')
                except Exception:
                    messages.error(request, "Username exists")
                    return render(request, 'Register.html')
            else:
                error_str = "Error: Passwords don't match"
                messages.error(request, error_str)
                return render(request, 'Register.html')

        else:
            error_str = "Error: "
            if name == "":
                error_str = error_str + '-Empty Name field! '
            if email == "":
                error_str = error_str + '-Empty Empty field! '
            if password == "":
                error_str = error_str + '-Empty Password field! '
            if re_password == "":
                error_str = error_str + '-Please Re-enter Password! '
            messages.error(request, error_str)
            return render(request, 'Register.html')
    else:
        return render(request, 'Register.html')
    
def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        if email != "" and password != "":
            try:
                customerInfo = register.objects.get(email = email)
                flag = check_password(password, customerInfo.password)
                # pass1 = customerInfo.password
                # if pass1 == password:
                if flag:
                    request.session['customer'] = customerInfo.username
                    response = redirect('/findme/main')
                    return response
                else:
                    error_str = "Error: Incorrect Password"
                    messages.error(request, error_str)
                    return render(request, 'login.html')
            except Exception:
                    messages.error(request, "You haven't been registered yet!")
                    return render(request, 'login.html')
        else:
            error_str = "Error: "
            
            if email == "":
                error_str = error_str + '-Empty Empty field! '
            if password == "":
                error_str = error_str + '-Empty Password field! '
            messages.error(request, error_str)
            return render(request, 'login.html')
    return render(request, 'login.html')

def forgot(request):
    return render(request, 'forgot.html')

def main(request):
    print('hello')
    customer = request.session['customer']
    products=add_product.objects.all()
    for product in products:
        product.vendor = contact_info.objects.get(vendor_id = product.vendor_id)
        print(product.vendor.mobile_no)
        # order.product = add_product.objects.get(product_id = order.product_id)

    vendors=contact_info.objects.all()
    
    context={
        'products':products,
        'vendors':vendors,
        'username': customer,
        # 'number':9448314115,
    }
    return render(request, 'main.html', context)


def products(request):
    customer = request.session['customer']
    products=add_product.objects.all()
    for product in products:
        product.vendor = contact_info.objects.get(vendor_id = product.vendor_id)
        print(product.vendor.mobile_no)
        # order.product = add_product.objects.get(product_id = order.product_id)

    vendors=contact_info.objects.all()
    
    context={
        'products':products,
        'vendors':vendors,
        'username': customer,
        # 'number':9448314115,
    }
    return render(request, 'products.html', context)

# def product(request):
#     customer = request.session['customer']
#     if request.method == "POST":
#         product_id = request.POST['id']
#         product = add_product.objects.get(product_id = product).product_name
#         print(product, 'hell')
#     # print(request.session['id'])
#     # allinfo = add_product.objects.filter(product_id = ).values()
#     # print(allinfo)

#     # return render(request, 'product.html', {'username': customer, 'allinfo':allinfo})
#     return render(request, 'product.html', {'username': customer})

def product(request, product_slug):
    customer = request.session['customer']
    try:
        product = add_product.objects.get(slug = product_slug)
        in_cart = CartItem.objects.filter(cart_id = register.objects.get(username = customer).user_id, product_id = product.product_id).exists()
        product.vendor = contact_info.objects.get(vendor_id = product.vendor_id)

    except Exception as e:
        raise e 

    try:
        user_id = register.objects.get(username = customer).user_id
        orderproduct = OrderProduct.objects.filter(user_id = user_id , product_id=product.product_id).exists()
    except OrderProduct.DoesNotExist:
        orderproduct=None
    #review
    reviews=ReviewRating.objects.filter(product_id=product.product_id, status__in=[True])
    

    context = {
        'username': customer,
        'product' : product,
        'in_cart' : in_cart,
        'orderproduct': orderproduct,
        'reviews':reviews
    }
    return render(request, 'product.html', context)


def _cart_id(request):
    cart = request.session.session_key
    print(cart, 'exxisting')
    if not cart:
        cart = request.session.create()
        print(cart, 'creating cart')
    return cart

def cart(request, total = 0, quantity = 0, cart_items = None, grand_total = 0, tax = 0):
    try:
        customer = request.session['customer']
        user_id = register.objects.get(username = customer).user_id
        # print(user_id)
        try:
            cart = Cart.objects.get(cart_id = user_id) # get the cart using the cart_id present in the session
            cart_items = CartItem.objects.filter(cart_id = cart.cart_id, is_active__in=[True] ).all()
            print(cart_items[0], 'hello')
            for cart_item in cart_items:
                print('Yellow')
                print(cart_item)
                total += (cart_item.Price * cart_item.quantity)
                quantity += cart_item.quantity 
            tax = 2 * total / 100
            grand_total = total + tax
        except Exception:
            pass
        context = {
            'username':customer,
            'total': total,
            'quantity': quantity,
            'cart_items': cart_items,
            'grand_total': grand_total,
            'tax':tax
        }
        return render(request, 'cart.html', context)
    except Exception:
        messages.error(request, "You haven't logged in yet!!")
        return render(request, 'login.html')
    # return render(request, 'cart.html', {'username': customer, 'context}':context})

def wishlist(request):
    customer = request.session['customer']
    user_id = register.objects.get(username = customer).user_id
    products = WishlistItem.objects.filter(wishlist_id = user_id)
    for each in products:
        each.product = add_product.objects.get(product_id = each.product_id)
    context = {
            'username':customer,
            'products':products,
        }
    return render(request, 'wishlist.html', context)
    
def add_wishlist(request, product_id):
    try:
        customer = request.session['customer']
        user_id = register.objects.get(username = customer).user_id
        product = add_product.objects.get(product_id = product_id) #get the product
        # cart_id = _cart_id(request)
        try:
            wishlist = Wishlist.objects.get(wishlist_id = user_id) # get the cart using the cart_id present in the session
        except Exception:
            wishlist = Wishlist(wishlist_id = user_id)
            wishlist.save()

        try:
            print('wishlistss', wishlist.wishlist_id)
            print(product_id)
            wishlist_item = WishlistItem.objects.get(product_id = product_id, wishlist_id = wishlist.wishlist_id)
        except Exception:
            # print('hello')
            wishlist_item = WishlistItem(user_id = user_id, product_id = product_id, product_name = product.product_name, product_image = product.product_image, Price = product.Price, Description = product.Description ,quantity = 1, wishlist_id = user_id)
            wishlist_item.save()
        
        # wishlistitem = WishlistItem.objects.filter(user_id = user_id)

        
        return redirect('wishlist')
    except Exception:
        messages.error(request, "You haven't logged in yet!!")
        return render(request, 'login.html')


def remove_wishlist_item(request, product_id):
    customer = request.session['customer']
    user_id = register.objects.get(username = customer).user_id
    try:
        wishlist = Wishlist.objects.get(wishlist_id = user_id)
        WishlistItem.objects.filter(product_id = product_id, wishlist_id = user_id).delete()  
        return redirect('wishlist')
    except Exception:
        messages.error(request, "You haven't logged in yet!!")
        return render(request, 'login.html')

def add_cart(request, product_id):
    try:
        customer = request.session['customer']
        user_id = register.objects.get(username = customer).user_id
        print(user_id)
        product = add_product.objects.get(product_id = product_id) #get the product
        # cart_id = _cart_id(request)
        try:
            cart = Cart.objects.get(cart_id = user_id) # get the cart using the cart_id present in the session
        except Exception:
            cart = Cart(cart_id = user_id)
            cart.save()

        try:
            cart_item = CartItem.objects.get(product_id = product.product_id, cart_id = cart.cart_id)
            cart_item.quantity += 1 
            CartItem.objects.filter(product_id = product.product_id, cart_id = cart.cart_id).update(quantity =cart_item.quantity)  
        except CartItem.DoesNotExist:
            cart_item = CartItem(user_id = user_id, product_id = product.product_id, product_name = product.product_name, product_image = product.product_image, Price = product.Price, Description = product.Description ,quantity = 1, cart_id = cart.cart_id)
            cart_item.save()
        
        product = add_product.objects.get(product_id = cart_item.product_id)
        print(product.product_name)
        # return render(request, 'cart.html')
        return redirect('cart')
    except Exception:
        messages.error(request, "You haven't logged in yet!!")
        return render(request, 'login.html')


def remove_cart(request, product_id):
    product = get_object_or_404(add_product, product_id=product_id)
    try:
        customer = request.session['customer']
        user_id = register.objects.get(username = customer).user_id
        print(user_id)
        try:
        #     if request.user.is_authenticated:
        #         cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        #     else:
            cart = Cart.objects.get(cart_id = user_id)
            cart_item = CartItem.objects.get(product_id = product.product_id, cart_id = cart)
            
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                CartItem.objects.filter(product_id = product.product_id, cart_id = cart.cart_id).update(quantity = cart_item.quantity)  
            else:
                cart_item.delete()
        except:
            pass
        # return render(request, 'cart.html')
        return redirect('cart')
    except Exception:
        messages.error(request, "You haven't logged in yet!!")
        return render(request, 'login.html')

def remove_cart_item(request, product_id):
    product = get_object_or_404(add_product, product_id=product_id)
    # if request.user.is_authenticated:
    #     cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    # else:
    try:
        customer = request.session['customer']
        user_id = register.objects.get(username = customer).user_id
        cart = Cart.objects.get(cart_id = user_id)
        # cart_item = CartItem.objects.get(product_id=product.product_id, cart_id = cart)
        CartItem.objects.filter(product_id = product.product_id, cart_id = cart.cart_id).delete()  
    
        return redirect('cart')
    except Exception:
        messages.error(request, "You haven't logged in yet!!")
        return render(request, 'login.html')


def checkout(request):
    customer = request.session['customer']
    user_id = register.objects.get(username = customer).user_id
    cart = Cart.objects.get(cart_id = user_id)
    cart_items = CartItem.objects.filter(cart_id = cart.cart_id, is_active__in=[True] ).all()
    context = {
        'username':customer,      
        'cart_items': cart_items,
                    
    }
    return render(request, 'checkout.html', context)
    # return render(request, 'checkout.html')

def place_order(request, total = 0, quantity = 0, grand_total = 0):
    # customer = request.session['customer']
    # try:
        customer = request.session['customer']
        cart = Cart.objects.get(cart_id = register.objects.get(username = customer).user_id)
        cart_items = CartItem.objects.filter(cart_id = cart.cart_id, is_active__in=[True] ).all()

        
        # return render(request, "checkout.html")
        if len(cart_items) <= 0:
            return redirect('products')

        for cart_item in cart_items:
            total += (cart_item.Price * cart_item.quantity)
            quantity += cart_item.quantity 

        tax = 2 * total / 100
        grand_total = total + tax
        if request.method == "POST":
            form = OrderForm(request.POST)
            if form.is_valid():
                user_id = register.objects.get(username = customer).user_id
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                phone = form.cleaned_data['phone']
                email = form.cleaned_data['email']
                address_line_1 = form.cleaned_data['address_line_1']
                address_line_2 = form.cleaned_data['address_line_2']
                country = form.cleaned_data['country']
                state = form.cleaned_data['state']
                city = form.cleaned_data['city']
                order_note = form.cleaned_data['order_note']
                order_total = grand_total
                tax = tax
                data=Order(user_id = register.objects.get(username = customer).user_id, first_name = first_name,
                last_name = last_name, phone = phone, email = email, address_line_1 = address_line_1, address_line_2 = address_line_2, country = country,
                state = state, city = city, order_note = order_note, order_total = order_total, tax = tax)
                #for user profile
                user_id1= register.objects.get(username = customer).user_id
                first_name1 = form.cleaned_data['first_name']
                last_name1 = form.cleaned_data['last_name']
                phone1 = form.cleaned_data['phone']
                email1 = form.cleaned_data['email']
                address_line_11 = form.cleaned_data['address_line_1']
                address_line_21 = form.cleaned_data['address_line_2']
                city1 = form.cleaned_data['city']
                state1 = form.cleaned_data['state']
                country1 = form.cleaned_data['country']
                data1=Profile(user_id = register.objects.get(username = customer).user_id ,first_name = first_name1,
                last_name = last_name1, phone = phone1, email = email1, address_line_1 = address_line_11, address_line_2 = address_line_21, country = country1,
                state = state1, city = city1)
                data.save()

                if Profile.objects.filter(user_id = register.objects.get(username = customer).user_id).exists():
                    Profile.objects.filter(user_id=register.objects.get(username = customer).user_id).update(first_name = first_name1,
                    last_name = last_name1, phone = phone1, email = email1, address_line_1 = address_line_11, address_line_2 = address_line_21, country = country1,
                    state = state1, city = city1)
                else:
                    data1.save()
                            
    
        # Order.objects.get(user_id = register.objects.get(user_id = register.objects.get(username = customer).user_id,, username = customer).user_id, is_ordered=False)..update(about=About)  
        order = Order.objects.get(user_id = register.objects.get(username = customer).user_id,is_ordered__in = ['False'] )
        # contact_info.objects.filter(email=email).update(about=About)            
        context = {
            'username':customer,
            'cart_items': cart_items,
            'order'   :order,
            'total': total,
            'grand_total': grand_total,
            'tax':tax
        }
        return render(request, 'place_order.html', context)
    
    # except Exception:
    #     messages.error(request, "You haven't logged in yettt!!")
    #     return render(request, 'login.html')
    # else:
    #         return render(request, 'place_order.html')



def review_place_order(request, total = 0, quantity = 0, grand_total = 0):
    customer = request.session['customer']
    user_id = register.objects.get(username = customer).user_id
    # order = Order.objects.filter(user_id = user_id, is_ordered__in = ['False'])
    Order.objects.filter(user_id = user_id, is_ordered__in = ['False']).update(is_ordered = True)  
    order = Order.objects.get(user_id = user_id, is_ordered__in = ['True'], status = 'New')
    print(order.order_id, 'orderhello')
    cart = Cart.objects.get(cart_id = register.objects.get(username = customer).user_id)
    cart_items = CartItem.objects.filter(cart_id = cart.cart_id, is_active__in=[True] ).all()
    for cart_item in cart_items:
        vendor_id = add_product.objects.get(product_id = cart_item.product_id).vendor_id
        orderproduct = OrderProduct(vendor_id = vendor_id,order_id = order.order_id, user_id = user_id, product_id = cart_item.product_id, quantity = cart_item.quantity, product_price = cart_item.Price, ordered = True, status = 'Placed')
        orderproduct.save()
        add_product.objects.filter(product_id = cart_item.product_id).update(stock = add_product.objects.get(product_id = cart_item.product_id).stock - cart_item.quantity)

    CartItem.objects.filter(cart_id = user_id).delete()
    Order.objects.filter(user_id = user_id, is_ordered__in = ['True'], status = 'New').update(status = 'Placed')
    return redirect('cart')

    
                

def search(request):
    customer = request.session['customer']
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        print('keyword', keyword)
        if keyword:
            product_register=add_product.objects.filter(Description__icontains = keyword)|add_product.objects.filter(product_name__icontains = keyword)
            vendors = contact_info.objects.filter(Person_name__icontains = keyword) | contact_info.objects.filter(company_name__icontains = keyword) | contact_info.objects.filter(about__icontains = keyword)
            print(len(product_register))
            product_count=product_register.count()
    return render(request, 'products.html', {'username': customer,'products':product_register, 'product_count':product_count, 'vendors':vendors})

def catagery(request, name):
    customer = request.session['customer']
    product_register=add_product.objects.filter(Description__icontains = name)
    product_count=product_register.count()
    return render(request, 'products.html', {'username': customer,'products':product_register, 'product_count':product_count})


def vendor_view(request, vendor_id):
    print('vendor_idss', vendor_id)
    vendor = contact_info.objects.get(vendor_id = vendor_id)
    products = add_product.objects.filter(vendor_id = vendor_id)
    # print(len(vendor), 'personss')
    context = {
        'vendor': vendor,
        'products':products,
    }
    return render(request, 'vendor_view.html', context)


    
# def add_cart(request, product_id):
#     product = add_product.objects.get(product_id = product_id) #get the product
#     cart_id = _cart_id(request)
#     try:
#         cart = Cart.objects.get(cart_id = cart_id) # get the cart using the cart_id present in the session
#     except Exception:
#         cart = Cart(cart_id = cart_id)
#         cart.save()

#     try:
#         cart_item = CItem.objects.get(product_id = product.product_id, cart_id = cart)
#         cart_item.quantity += 1 
#         # CItem.objects.filter(product_id = product.product_id, cart_id = cart.cart_id).update(quantity =cart_item.quantity)  
#     except CItem.DoesNotExist:
#         cart_item = CItem(product_id = product.product_id, quantity = 1, cart_id = cart.cart_id)
#         cart_item.save()
    
#     product = add_product.objects.get(product_id = cart_item.product_id)
#     return redirect('cart')

# def add_cart(request, product_id):
#     # current_user = request.customer 
#     product = add_product.objects.get(id=product_id) #get the product
#     # If the user is authenticated
#     if current_user.is_authenticated:
#         product_variation = []
#         if request.method == 'POST':
#             for item in request.POST:
#                 key = item
#                 value = request.POST[key]

#                 try:
#                     variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
#                     product_variation.append(variation)
#                 except:
#                     pass


#         is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
#         if is_cart_item_exists:
#             cart_item = CartItem.objects.filter(product=product, user=current_user)
#             ex_var_list = []
#             id = []
#             for item in cart_item:
#                 existing_variation = item.variations.all()
#                 ex_var_list.append(list(existing_variation))
#                 id.append(item.id)

#             if product_variation in ex_var_list:
#                 # increase the cart item quantity
#                 index = ex_var_list.index(product_variation)
#                 item_id = id[index]
#                 item = CartItem.objects.get(product=product, id=item_id)
#                 item.quantity += 1
#                 item.save()

#             else:
#                 item = CartItem.objects.create(product=product, quantity=1, user=current_user)
#                 if len(product_variation) > 0:
#                     item.variations.clear()
#                     item.variations.add(*product_variation)
#                 item.save()
#         else:
#             cart_item = CartItem.objects.create(
#                 product = product,
#                 quantity = 1,
#                 user = current_user,
#             )
#             if len(product_variation) > 0:
#                 cart_item.variations.clear()
#                 cart_item.variations.add(*product_variation)
#             cart_item.save()
#         return redirect('cart')
#     # If the user is not authenticated
#     else:
#         product_variation = []
#         if request.method == 'POST':
#             for item in request.POST:
#                 key = item
#                 value = request.POST[key]

#                 try:
#                     variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
#                     product_variation.append(variation)
#                 except:
#                     pass


#         try:
#             cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
#         except Cart.DoesNotExist:
#             cart = Cart.objects.create(
#                 cart_id = _cart_id(request)
#             )
#         cart.save()

#         is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
#         if is_cart_item_exists:
#             cart_item = CartItem.objects.filter(product=product, cart=cart)
#             # existing_variations -> database
#             # current variation -> product_variation
#             # item_id -> database
#             ex_var_list = []
#             id = []
#             for item in cart_item:
#                 existing_variation = item.variations.all()
#                 ex_var_list.append(list(existing_variation))
#                 id.append(item.id)

#             print(ex_var_list)

#             if product_variation in ex_var_list:
#                 # increase the cart item quantity
#                 index = ex_var_list.index(product_variation)
#                 item_id = id[index]
#                 item = CartItem.objects.get(product=product, id=item_id)
#                 item.quantity += 1
#                 item.save()

#             else:
#                 item = CartItem.objects.create(product=product, quantity=1, cart=cart)
#                 if len(product_variation) > 0:
#                     item.variations.clear()
#                     item.variations.add(*product_variation)
#                 item.save()
#         else:
#             cart_item = CartItem.objects.create(
#                 product = product,
#                 quantity = 1,
#                 cart = cart,
#             )
#             if len(product_variation) > 0:
#                 cart_item.variations.clear()
#                 cart_item.variations.add(*product_variation)
#             cart_item.save()
#         return redirect('cart')
def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    user_id=request.session['customer']
    if request.method=="POST":
        
        if ReviewRating.objects.filter(user_id=user_id, product_id=product_id).exists():
                subject=request.POST['subject']
                rating=request.POST['rating']
                review=request.POST['review']
                ReviewRating.objects.filter(user_id=user_id, product_id=product_id).update(subject=subject, rating=rating, review=review)
                messages.success(request, 'Thank you! Your review has been updated.')
                return redirect(url)
        
        else:
            form=ReviewForm(request.POST)
            if form.is_valid():
                data=ReviewRating()
                data.subject=form.cleaned_data['subject']
                data.rating=form.cleaned_data['rating']
                data.review=form.cleaned_data['review']
                data.ip=request.META.get('REMOTE_ADDR')
                data.product_id=product_id
                data.user_id=user_id
                data.save()
                messages.success(request,  'Thank you! Your review has been submitted.')
                return redirect(url)

def my_orders(request):
    customer = request.session['customer']
    user_id = register.objects.get(username = customer).user_id
    orders=Order.objects.filter(user_id = user_id , is_ordered__in=[True]).order_by('-created_at')
    context={
        'orders':orders,
        'username':customer
    }
    return render(request, 'my_orders.html', context)

def edit_profile(request):
    customer = request.session['customer']
    user_id = register.objects.get(username = customer).user_id
    if request.method=='POST':
        user_id = register.objects.get(username = customer).user_id
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        phone=request.POST['phone']
        email=request.POST['email']
        address_line_1=request.POST['address_line_1']
        address_line_2=request.POST['address_line_2']
        city=request.POST['city']
        state=request.POST['state']
        country=request.POST['country']
        Profile.objects.filter(user_id=user_id).update(first_name=first_name, last_name=last_name, phone=phone,
        email=email,address_line_1=address_line_1,address_line_2=address_line_2,city=city, state=state, country=country)
        messages.success(request, "profile updated")
        return redirect('edit_profile')

    updated=Profile.objects.get(user_id = user_id)

    context={
        'user_profile':updated,
        'username':customer,
        
    }   
        
    return render(request, 'edit_profile.html', context)

def order_detail(request, order_id):
    customer = request.session['customer']
    order_detail=OrderProduct.objects.filter(order_id=order_id)
    order=Order.objects.get(order_id=order_id)
    for orders in order_detail:
        orders.product = add_product.objects.get(product_id = orders.product_id)
        
    subtotal=0
    print(order_detail[0].product.product_name, 'jjjyyyy')
    for i in order_detail:
        subtotal+= i.product_price*i.quantity
    context={
        'order_detail':order_detail,
        'order':order,
        'username':customer,
        'subtotal':subtotal,
    }
    return render(request, 'order_detail.html', context)

def logout(request): 
    try:
        del request.session['customer']
        return render(request, 'login.html', {'message':'You have been successfully logged out!'})
    except Exception:
        return redirect('login')