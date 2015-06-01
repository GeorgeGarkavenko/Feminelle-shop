from django.db import models
from main.models import Product

class News(models.Model):
    
    title = models.CharField(max_length=255)
    text = models.TextField(null=True, blank=True)
    
    author = models.CharField(max_length=50, null=True, blank=True)
    
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
        
    def __unicode__(self):
        return '(%s %d:%d) %s' % (self.date.date(),
                                   self.date.hour,
                                   self.date.minute,
                                   self.title,)
    
class Review(models.Model):

    title = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField()
    
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    author_hided = models.BooleanField(default=False)
    
    accepted = models.BooleanField(default=False)
    
    product = models.ForeignKey(Product, related_name='related_product', null=True, blank=True)    
        
    def __unicode__(self):
        return '(%s %d:%d) %s: %s%s' % (self.date.date(),
                                   self.date.hour,
                                   self.date.minute,
                                   self.name if self.name else self.email,
                                   self.title if self.title else self.text[:10],
                                   '' if self.title else '...')

class Message(models.Model):

    title = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField()
    
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
        
    send_back = models.BooleanField(default=False)
    
    def __unicode__(self):
        return '(%s %d:%d) %s: %s%s' % (self.date.date(),
                                   self.date.hour,
                                   self.date.minute,
                                   self.name if self.name else self.email,
                                   self.title if self.title else self.text[:10],
                                   '' if self.title else '...')
