from .models import Cart, CartItem
from .views import _cart_id
from customers.models import *

def counter(request):
    try:
        customer = request.session['customer']
        user_id = register.objects.get(username = customer).user_id
        
        cart_count = 0
        if 'admin' in request.path:
            return {}
        else:
            try:
                # cart = Cart.objects.get(cart_id = _cart_id(request))
                cart = Cart.objects.get(cart_id = user_id)

                if request.user.is_authenticated:
                    cart_items = CartItem.objects.all().filter(user=request.user)
                else:
        
                    cart_items = CartItem.objects.filter(cart_id = cart)
                    # print('hello', cart_items[0])
                    for cart_item in cart_items:
                        cart_count += cart_item.quantity
            except Exception as e:
                cart_count = 0
                # print('helloyyy')
            
            # print('hello', cart_count)
        return dict(cart_count=cart_count)
    except Exception as e:
        cart_count = 0
                # print('helloyyy')
            