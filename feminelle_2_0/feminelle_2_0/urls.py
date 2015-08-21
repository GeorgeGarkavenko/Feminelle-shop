from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin

import main.views

import info.views


admin.autodiscover()

urlpatterns = patterns('',
    
    # main
    url(r'^$', main.views.home, name='home'),
    
    url(r'^catalogue/$', main.views.catalogue, name='catalogue'),
    url(r'^catalogue/all$', main.views.products, name='productsAll', kwargs={'new_selection': True}),
    url(r'^catalogue/all/(?P<page>\d+)$', main.views.products, name='productsAll_transition', kwargs={'new_selection': False}),
    
    url(r'^catalogue/(?P<pk>\d+)$', main.views.product, name='product'),
    
    # product_class argument 'a,b,c|d,e,f' logic is is '(a or b or c) and d and e and f' (| is filter)
    # special classes: novelties, promo
    url(r'^catalogue/(?P<product_class>[|,a-zA-Z_]+)$', main.views.products, name='product_class', kwargs={'new_selection': True}),
    url(r'^catalogue/(?P<product_class>[|,a-zA-Z_]+)/(?P<page>\d+)$', main.views.products, name='product_class_transition', kwargs={'new_selection': False}),
   
    url(r'^order/$', main.views.order, name='order'),
    
    # info
    url(r'^news/$', info.views.news, name='news'),
     
    url(r'^articles/$', info.views.articles, name='articles'),
    url(r'^articles/sizes_table$', info.views.sizes_table, name='sizes_table'),
    url(r'^articles/(?P<article>[-_\w]+)$', info.views.article, name='article'), 
    
    url(r'^reviews/(?P<page>\d+)$', info.views.reviews, name='reviews'),
   
    url(r'^contact/$', info.views.contact, name='contact'),
    url(r'^history/$', info.views.history, name='history'),
    url(r'^sitemap/$', info.views.sitemap, name='sitemap'),
    
    # other
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^captcha/', include('captcha.urls')),
)

urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)