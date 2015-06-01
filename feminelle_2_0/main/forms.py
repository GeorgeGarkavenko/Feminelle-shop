from django import forms
from captcha.fields import CaptchaField

class OrderForm(forms.Form):
    #email*,
    #name,
    #city,
    #address,
    #phone*,
    #fax
    #(sizes: bosoms, grouth, hips),
    #delivery,
    #payment,
    #note,
    
    email = forms.EmailField(label='E-mail*')
    
    name = forms.CharField(label='Your name', required=False, max_length=50)
    
    city = forms.CharField(label='Your city', required=False, max_length=25)
    
    address = forms.CharField(label='Your address', required=False, max_length=100)
    
    phone = forms.IntegerField(label='Your phone', required=False)
    
    fax = forms.IntegerField(label='Your fax', required=False)
    
    bosoms = forms.IntegerField(label='bosoms', required=False)
    
    grouth = forms.IntegerField(label='grouth', required=False)    
    
    hips = forms.IntegerField(label='hips', required=False)
    
    delivery = forms.CharField(label='delivery type', max_length=25)
    
    payment = forms.CharField(label='payment type', max_length=25)
    
    note = forms.CharField(label='Any requirement',widget=forms.Textarea, required=False)
    
    captcha = CaptchaField()
    