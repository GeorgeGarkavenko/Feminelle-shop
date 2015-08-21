from django.contrib import admin

from .models import (Address,
                     Customer,
                     Ordered_product,
                     Product,
                     Product_image,
                     Product_class,
                     Product_color,
                     Product_size,
                     Purchase_order)
# Inlines     
class AddressInline(admin.TabularInline):
    model = Address
    extra = 3

class Ordered_productInline(admin.TabularInline):
    model = Ordered_product
    extra = 3

class ImageInline(admin.TabularInline):
    model = Product_image
    extra = 3
    
class OrdersInline(admin.TabularInline):
    model = Purchase_order
    extra = 3

# Admins
class Customer_admin(admin.ModelAdmin):
    list_display = ['__unicode__']
    inlines = [AddressInline, OrdersInline]
    class Meta:
        model = Customer
        

class Ordered_product_admin(admin.ModelAdmin):
    list_display = ['__unicode__']
    class Meta:
        model = Ordered_product
      

class Product_admin(admin.ModelAdmin):
    list_display = ['__unicode__',
                    #'get_class', 'promotion','get_colors',
                    #'image',
                    'timestamp', 'modtime']
    inlines = [ImageInline]
    
    #raw_id_fields = ("product_color",)
    
    class Meta:
        model = Product
        
class Product_class_admin(admin.ModelAdmin):
    list_display = ['__unicode__']
    class Meta:
        model = Product_class

        
class Product_color_admin(admin.ModelAdmin):
    list_display = ['id', '__unicode__']
    
    ordering = ('name',)
    class Meta:
        model = Product_color

        
class Product_size_admin(admin.ModelAdmin):
    list_display = ['__unicode__']
    class Meta:
        model = Product_size


class Purchase_order_admin(admin.ModelAdmin):
    list_display = ['__unicode__']
    inlines = [Ordered_productInline]
    class Meta:
        model = Purchase_order
        

# Register sites

admin.site.register(Customer, Customer_admin)

admin.site.register(Ordered_product, Ordered_product_admin)

admin.site.register(Product, Product_admin)

admin.site.register(Product_class, Product_class_admin)

admin.site.register(Product_color, Product_color_admin)

admin.site.register(Product_size, Product_size_admin)

admin.site.register(Purchase_order, Purchase_order_admin)