from django.urls import URLPattern, path, re_path
from django.contrib import admin
from . import views
import vendor.views 

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.login, name='login'),
    path('Register', views.Register, name='Register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('main', views.main, name='main'),
    path('home', views.home, name='home'),
    path('forgot', views.forgot, name='forgot'),
    path('add_cart/<str:product_id>/', views.add_cart, name='add_cart'),
    path('remove_cart/<str:product_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<str:product_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('wishlist', views.wishlist, name='wishlist'),
    path('add_wishlist/<str:product_id>/', views.add_wishlist, name='add_wishlist'),
    path('remove_wishlist_item/<str:product_id>/', views.remove_wishlist_item, name='remove_wishlist_item'),
    path('cart', views.cart, name='cart'),
    path('products', views.products, name='products'),
    path('product', views.product, name='product'),
    path('checkout', views.checkout, name='checkout'),
    path('place_order', views.place_order, name='place_order'),
    path('vendor_view/<str:vendor_id>', views.vendor_view, name='vendor_view'),
    path('review_place_order', views.review_place_order, name='review_place_order'),
    path('product/<slug:product_slug>/', views.product, name='product'),
    path("search/", views.search, name="search"),
    re_path(r'^catagery/(?P<name>\w+)/$', views.catagery, name="catagery"),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('submit_review/<str:product_id>/', views.submit_review, name="submit_review"),
    # path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('order_detail/<str:order_id>/', views.order_detail, name='order_detail'),
]
