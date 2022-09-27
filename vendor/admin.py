from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(register)
admin.site.register(Order)
admin.site.register(OrderProduct)
# admin.site.register(register)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    # prepopulated_fields = {'slug': ('product_name',)}
    # inlines = [ProductGalleryInline]
# class CategoryAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('category_name',)}
#     list_display = ('category_name', 'slug')
