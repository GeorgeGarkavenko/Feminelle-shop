from django.contrib import admin

from .models import (News,
                     Review,
                     Message)


class News_admin(admin.ModelAdmin):
    list_display = ['__unicode__']
    class Meta:
        model = News
        
class Review_admin(admin.ModelAdmin):
    list_display = ['__unicode__']
    class Meta:
        model = Review
   
class Message_admin(admin.ModelAdmin):
    list_display = ['__unicode__']
    class Meta:
        model = Message
        
# Register sites

admin.site.register(News, News_admin)

admin.site.register(Review, Review_admin)

admin.site.register(Message, Message_admin)