
from django.db import models

from .catalogue import DELIVERY, PAYMENT

# posible Product parameters    
class Product_class(models.Model):
    name = models.CharField(max_length=225, unique=True)
    
    def __unicode__(self):
            return '%s' % (self.name)
    
class Product_color(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __unicode__(self):
            return '%s' % (self.name)
  
class Product_size(models.Model):
    name = models.CharField(max_length=20, unique=True)
    
    def __unicode__(self):
            return '%s' % (self.name)
   
# record of product order 
class Product(models.Model):
    
    # codes

    article = models.CharField(max_length=25, null=True, blank=True, default='AA0011')
    code = models.IntegerField(null=True, blank=True)
    
    position = models.IntegerField(null=True, blank=True, default=1)  
    
    # name info
    name = models.CharField(max_length=225)
    
    product_class = models.ManyToManyField(Product_class, related_name='product_class+', null=True, blank=True)
    
    manufacturer = models.CharField(max_length=100, default='feminelle')
    
    # parameters info
    season = models.CharField(max_length=25, null=True, blank=True)
    
    product_color = models.ManyToManyField(Product_color, related_name='product_color', null=True, blank=True)
    
    product_size = models.ManyToManyField(Product_size, related_name='product_size', null=True, blank=True)
   
    image = models.FileField(upload_to='product_title_pictures', null=True, blank=True)
   
    structure = models.CharField(max_length=255, null=True, blank=True)
    
    description = models.TextField(null=True, blank=True)
   
    # purchase info
    promotion = models.CharField(max_length=225, null=True, blank=True)
    promotioin_modifier = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    reserve = models.IntegerField(default=0)
    
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    popularity = models.IntegerField(default=0)
    
    note = models.TextField(null=True, blank=True)
    
    # time notes
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    modtime = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    # display permission
    accepted = models.BooleanField(default=True)
    
    def __unicode__(self):
        
        if False: #self.product_class:
            product_class=','.join(set(obj.name for obj in self.product_class.all()) )
            
            return '%s: %s' % (product_class, self.name)
        else:
            return '%s' % (self.name)
    
    def has_description(self):
        return bool(self.description)
    
    def has_note(self):
        return bool(self.note)
        
class Product_image(models.Model):
    
    reference = models.FileField(upload_to='product_pictures', null=True, blank=True)
    
    product = models.ForeignKey(Product, related_name='product')
    
    description = models.TextField(null=True, blank=True)
    
    def __unicode__(self):
            return 'Image # %d' % (self.id)   
  
class Customer(models.Model):
    
    email = models.EmailField(default='noname@world.net', unique=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    
    bosoms = models.IntegerField(null=True, blank=True)
    grouth = models.IntegerField(null=True, blank=True)   
    hips = models.IntegerField(null=True, blank=True)
    
    promotioin = models.CharField(max_length=225, default='ordinary')
    promotioin_modifier = models.DecimalField(max_digits=30, decimal_places=8, default=1)
    
    registration_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    def __unicode__(self):
        return '%s' % (self.name if self.name else self.email)

class Address(models.Model):

    customer = models.ForeignKey(Customer, related_name='address_owner')

    city = models.CharField(max_length=25, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    
    fax = models.IntegerField(null=True, blank=True) 
    phone = models.IntegerField(null=True, blank=True)
    
    def __unicode__(self):
        if (self.city and self.address):    
            return '%s, %s' % (self.city, self.address)
        else:
            return '%s' % (self.phone)
   
    
class Purchase_order(models.Model):

    customer =  models.ForeignKey(Customer, related_name='purchase_owner')
    
    delivery = models.CharField(max_length=20, choices=DELIVERY)
    payment = models.CharField(max_length=20, choices=PAYMENT)
    
    note = models.TextField(null=True, blank=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    satisfied = models.NullBooleanField()

    def __unicode__(self):
        return "Purchase from %s on %s %d:%d, total = %d"\
            % (self.customer.__unicode__(),
                    self.timestamp.date(), 
                    self.timestamp.hour,
                    self.timestamp.minute,
                    self.price)
  
  
class Ordered_product(models.Model):
    
    order = models.ForeignKey(Purchase_order, related_name='order_reference', null=True, blank=True)
    
    product = models.ForeignKey(Product, related_name='product_name')
    
    size = models.ForeignKey(Product_size, related_name='order_product_size', null=True, blank=True)
    
    color = models.ForeignKey(Product_color, related_name='order_product_color', null=True, blank=True)
    
    quantity = models.IntegerField(default=1)
    
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)    
     
    def __unicode__(self):
        
        return "Record # %d: product # %d" % (self.id if self.id else 0, self.product_id if self.product_id else 0)

