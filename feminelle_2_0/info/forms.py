from django import forms
from .models import Message, Review

from captcha.fields import CaptchaField

class MessageForm(forms.ModelForm):
    
    captcha = CaptchaField()
    
    class Meta:
        model = Message
        fields = ["name", "email", "title", "text", "send_back",]
        
class ReviewForm(forms.ModelForm):
    
    captcha = CaptchaField()
    
    class Meta:
        model = Review
        fields = ["name", "email", "title", "text", "author_hided",]