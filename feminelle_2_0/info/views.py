from django.contrib import messages
# pagination
from django.core.paginator import Paginator
# templates rendering
from django.core.urlresolvers import reverse, reverse_lazy

from django.shortcuts import ( render,
                              HttpResponseRedirect,
                              get_object_or_404,
                              get_list_or_404,
                              Http404)

# import basket funtionality
from main.views import handle_basket_query, get_basket_products, get_badges_info
#==========================

from .forms import MessageForm, ReviewForm

from .models import News, Review, Message

from .messages import MESSAGES

from main.models import Product

REVIEWS_FOR_PAGE = 5

def news(request):
    
    if handle_basket_query(request):
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    context = { 'object_list': sorted(News.objects.all(), key=lambda item: item.date, reverse=True),
                'basket_products': get_basket_products(request),
                'badges_info': get_badges_info(request) }
    
    template = 'news.html'
    return render(request, template, context)

def newsItem(request, pk):
    
    if handle_basket_query(request):
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    try:
        context = { 'object': get_object_or_404(News, id=int(pk)),
                    'basket_products': get_basket_products(request),
                    'badges_info': get_badges_info(request) }
    except:
        raise Http404
    
    template = 'newsItem.html'
    return render(request, template, context)

def reviews(request, page):
    
    if handle_basket_query(request):
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    if request.method == 'POST' and request.POST.get('form_name') == 'review':
        # create a form instance and populate it with data from the request:
        form = ReviewForm(request.POST)
        # check whether it's valid:
        
        if form.is_valid():
            # create new review
            Review.objects.create(
                title = form.cleaned_data['title'],
                text = form.cleaned_data['text'],
                
                name = form.cleaned_data['name'],
                email = form.cleaned_data['email'],
                author_hided = form.cleaned_data['author_hided']
            )
            
            messages.success(request, MESSAGES['review_accepted'])

            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    else:
        form = ReviewForm(initial=dict((k, '') for k in ReviewForm().fields.keys()))
    
    
    paginator = Paginator(sorted(Review.objects.filter(accepted = True), key=lambda r: r.date, reverse=True), REVIEWS_FOR_PAGE)
    
    pages_range = tuple(n + 1 for n in range(paginator.num_pages))
    
    try:
        if not (int(page) in pages_range):
            raise Http404
    except:
        raise Http404
    
    reviews_list = tuple({'review': item, 'product': Product.objects.get(id=item.product_id) if item.product_id else None} 
        for item in paginator.page(int(page)).object_list)
    
    context = { 'page_name': 'reviews',
                'object_list': reviews_list,
                'page_number': int(page),
                'page_surround': {'previous': int(page)-1,
                                  'next': 'none' if int(page) == paginator.num_pages else int(page)+1},
                'pages_range': pages_range,
                'form': form,
                'basket_products': get_basket_products(request),
                'badges_info': get_badges_info(request) }    
    
    template = 'reviews.html'
    return render(request, template, context)


def articles(request):
    
    if handle_basket_query(request):
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    context = {'basket_products': get_basket_products(request),
               'badges_info': get_badges_info(request) }
    
    template = 'articles.html'
    return render(request, template, context)

def sizes_table(request):
    
    if handle_basket_query(request):
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    context = {'basket_products': get_basket_products(request),
               'badges_info': get_badges_info(request) }
    
    template = 'sizes_table.html'
    return render(request, template, context)

def article(request, article):
    
    if handle_basket_query(request):
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    context = {'basket_products': get_basket_products(request),
               'badges_info': get_badges_info(request) }
    
    template = 'article_' + str(article) + '.html'
    return render(request, template, context)
    
def contact(request):
    
    if handle_basket_query(request):
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    if request.method == 'POST' and request.POST.get('form_name') == 'contact':
        # create a form instance and populate it with data from the request:
        form = MessageForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            
            # create new review
            Message.objects.create(
                title = form.cleaned_data['title'],
                text = form.cleaned_data['text'],
                
                name = form.cleaned_data['name'],
                email = form.cleaned_data['email'],
                send_back = form.cleaned_data['send_back']
            )
            
            messages.success(request, MESSAGES['message_accepted'])

            return HttpResponseRedirect(request.META['HTTP_REFERER'])

    else:
        form = MessageForm(initial=dict((k, '') for k in MessageForm().fields.keys()))
    
    context = { 'form': form,
                'basket_products': get_basket_products(request),
                'badges_info': get_badges_info(request) }    
    
    template = 'contact.html'
    return render(request, template, context)

def history(request):
    
    if handle_basket_query(request):
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    context = {'basket_products': get_basket_products(request),
               'badges_info': get_badges_info(request) }
    
    template = 'history.html'
    return render(request, template, context)

def sitemap(request):
    
    if handle_basket_query(request):
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    context = {'basket_products': get_basket_products(request),
               'badges_info': get_badges_info(request) }
    
    template = 'sitemap.html'
    return render(request, template, context)