from datetime import timedelta
from decimal import Decimal
from django.contrib import messages
# pagination
from django.core.paginator import Paginator

from django.conf import settings
# templates rendering
from django.core.urlresolvers import reverse, reverse_lazy
# email validators

from django.core.exceptions import ValidationError
# for filtering
from django.db.models import Q
# filtering & std
from django.shortcuts import ( render,
                              HttpResponseRedirect,
                              get_object_or_404,
                              get_list_or_404,
                              Http404)

#import forms

from .forms import OrderForm
from info.forms import ReviewForm

from django.views.generic import (
	DetailView,
	ListView,
)

from .models import (
    Address,
    Customer,
    Ordered_product,
    Product,
    Product_image,
    Product_color,
    Product_class,
    Product_size,
    Purchase_order,
)

from info.models import Message, News, Review

# Some functions

def getProductsAND(productClass, startProductList=None):
    """
    Out Products list with all <productClass> classes
    productClass is list of strings
    """
    products_list_accepted = Product.objects.filter(accepted=True)
    
    if startProductList:
        resultList = startProductList.filter(accepted=True)
    else: 
        resultList = products_list_accepted
    
    if products_list_accepted:
        # get day before last product add date
        modTimes = max(item.modtime for item in products_list_accepted)
        modTimes -= timedelta(days=1)
        
        for className in productClass:
            if className == 'novelties':
                
                # get next products list by modTimes (as novelties)
                resultList = resultList.filter(timestamp__gt=modTimes)
            else:
                resultList = resultList.filter(product_class__name=className)
            
    return resultList
    
def getProductsOR(productClass, startProductList=None):
    """
    Out Products list with any of <productClass> classes
    productClass is list of strings
    """
    
    products_list_accepted = Product.objects.filter(accepted=True)
    
    if products_list_accepted:
        if 'novelties' in productClass:
            # get day before last product add date
            
            modTimes = max(item.timestamp for item in products_list_accepted)
            modTimes -= timedelta(days=1)
            # get next products list by modTimes (as novelties)
     
            if startProductList:
                resultList = startProductList.filter(Q(accepted=True), Q(product_class__name__in=productClass) | Q(timestamp__gt=modTimes))
            else: 
                resultList=Product.objects.filter(Q(accepted=True), Q(product_class__name__in=productClass) | Q(timestamp__gt=modTimes))
        
        else:
            if startProductList:
                resultList = startProductList.filter(accepted=True, product_class__name__in=productClass)
            else: 
                resultList=Product.objects.filter(accepted=True, product_class__name__in=productClass)
    else:
        resultList = products_list_accepted
    
    return resultList

# basket functionality
def get_basket_products(request):
    
    object_list = []
    
    cycle = 0
    for porduct in request.session.get('basket_products', []):
        object_list.append({
            'product_id': get_object_or_404(Product, id=porduct['product_id']),
            'size': get_object_or_404(Product_size, name=porduct['size']) if porduct['size'] else None,
            'color': get_object_or_404(Product_color, name=porduct['color']) if porduct['color'] else None,
            'quantity': porduct['quantity'],
            'price': porduct['price'],
            'view_cycle': cycle
        })
        
        cycle = 0 if cycle == 2 else cycle + 1
        
    return object_list

def handle_basket_query(request):

    if request.method == 'POST' and request.POST.get('form_name') == 'basket':

        try:
            list_id = int(request.POST.get('list_id'))
        except:
            messages.error(request, 'Incorrect list index')
  
        if request.POST.get('action_todo', '') == 'remove':
            del request.session['basket_products'][list_id]
            
            # save changesin session
            request.session.modified = True
            
        elif request.POST.get('action_todo', '') == 'update':
            try:
                quantity = int(request.POST.get('quantity', 0))
 
                if quantity > 0:  
                    obj = request.session['basket_products'][list_id]
                    obj['quantity'] = quantity
                    obj['price'] = float(get_object_or_404(Product, id=obj['product_id']).price * quantity)
                    
                    # save changesin session
                    request.session.modified = True
                    
                else:
                    messages.error(request, 'Number must be positive (position # %d)' % (list_id + 1) )

            except:
                messages.error(request, 'Incorrect number: "%s" (position # %d)' %
                      (request.POST.get('quantity', '0'), list_id + 1 ) )
        
        return True
    # make a copy
    return False

def get_badges_info(request):
    return {
        # navbar
        'reviews':          Review.objects.filter(accepted=True).count(),
        'basket_count':     sum(product['quantity'] for product in request.session.get('basket_products', [])),
        'news':             News.objects.count(),
        'articles':         0,
        'messages':         Message.objects.count(),
        
        # sidebar
        'novelties':        getProductsOR(['novelties']).count(),
        'promo':            getProductsOR(['promo']).count(),
        'dress_sarafan':    getProductsOR(['dress', 'sarafan']).count(),
        'pants':            getProductsOR(['pants']).count(),
        'jeans':            getProductsOR(['jeans']).count(),
        'skirt':            getProductsOR(['skirt']).count(),
        'blouse_cardigan':  getProductsOR(['blouse', 'cardigan']).count(),
        'tunic':            getProductsOR(['tunic']).count(),
        'underwear':        getProductsOR(['underwear']).count(),
        'sport':            getProductsOR(['sport']).count(),
        'warm':             getProductsOR(['warm']).count(),
        'coveralls':        getProductsOR(['coveralls']).count(),
        'coat_poncho_jacket': getProductsOR(['coat', 'poncho','jacket']).count(),
        'all':              Product.objects.filter(accepted=True).count()
    }

# VIEWS


def home(request):
    
    if handle_basket_query(request):
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    print Product.objects.get(id=1, accepted=True).timestamp
    context = {'basket_products': get_basket_products(request),
               'badges_info': get_badges_info(request) }
    template = 'home.html'
    return render(request, template, context)
    
def catalogue(request):
    
    if handle_basket_query(request):
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    context = {'basket_products': get_basket_products(request),
               'badges_info': get_badges_info(request) }
    
    template = 'catalogue.html'
    return render(request, template, context)


def products(request, new_selection, product_class=None, page=1):
    
    if handle_basket_query(request):
        
        if (product_class is None):
            return HttpResponseRedirect(reverse('productsAll_transition', kwargs={'page': page}))
        else :
            return HttpResponseRedirect(reverse('product_class_transition', kwargs={'product_class': product_class, 'page': page}))

    # get session parameters for sorting
    if not request.session.get('sort_order'):
        # initial state
        request.session['sort_order'] = {
            'orderby': 'name',
            'limit': 10,
            'order_type': 'asc'
        }
    else:
        if request.method == 'POST' and request.POST.get('form_name') == 'sort':
        
            request.session['sort_order']['orderby'] = request.POST.get('orderby', 'name')
            
            try:
                request.session['sort_order']['limit'] = int(request.POST.get('limit'))
            except:
                request.session['sort_order']['limit'] = 10
        
            if request.POST.get('order_type', 'none') != 'none':
                
                if request.session['sort_order']['order_type'] == 'asc':
                    request.session['sort_order']['order_type'] = 'desc'
                
                else:
                    request.session['sort_order']['order_type'] = 'asc'
                    
            # save changesin session
            request.session.modified = True
            
            if (product_class is None):
                return HttpResponseRedirect(reverse('productsAll_transition', kwargs={'page': page}))
            else :
                return HttpResponseRedirect(reverse('product_class_transition', kwargs={'product_class': product_class, 'page': page}))
    
    
    if new_selection or request.session.get('products_selection') is None:
        
        # get products
        if product_class:
                
            product_class_str = product_class.split('|')
    
            if product_class_str[0] != '':
                resultSet = getProductsOR(product_class_str[0].split(','))
            
            if len(product_class_str) > 1:
                if product_class_str[0] != '':
                    resultSet = getProductsAND(product_class_str[1].split(','), resultSet)
                else:
                    resultSet = getProductsAND(product_class_str[1].split(','))
        else:
            # search result products list
            if request.method == 'GET' and request.GET.get('form_name') == 'search'\
                    and request.GET.get('search'):
                
                search_query = request.GET.get('search').strip().lower().split()
                
                print search_query
                
                #product_class
                #product_color
                #product_size
                
                
                
                query = Q(product_class__name__in=search_query)|\
                        Q(product_color__name__in=search_query)|\
                        Q(product_size__name__in=search_query)
                
                #article
                #name
                #manufacturer
                #season
                #structure
                #description
                #promotion
                #note    
                
                for word in search_query:
                    query = query |\
                        Q(article__icontains=word)|\
                        Q(name__icontains=word)|\
                        Q(manufacturer__icontains=word)|\
                        Q(season__icontains=word)|\
                        Q(structure__icontains=word)|\
                        Q(description__icontains=word)|\
                        Q(promotion__icontains=word)|\
                        Q(note__icontains=word)
                    
                resultSet = set(Product.objects.filter(Q(accepted=True),query))    
            else:
                resultSet = Product.objects.filter(accepted=True)
        
        # save resultSet to the
        request.session['products_selection'] = {'products_id': tuple(p.id for p in resultSet)}
        # save changesin session
        request.session.modified = True
        
        resultSet = list(resultSet)
        print resultSet
        
    else:
        # use previous selection
        resultSet = Product.objects.filter(id__in=request.session['products_selection']['products_id'])
        
    print new_selection, request.session.get('products_selection')

    # form context
    context = {
        'basket_products': get_basket_products(request),
        'badges_info': get_badges_info(request),
        'order_type_icon': request.session['sort_order']['order_type'],
        'orderby_select': {'name': '', 'timestamp': '',
                            'price': '', 'popularity': '' },
        'limit_select': {'v_1': '', 'v_2': '',
                        'v_5': '', 'v_10': '', 'v_15': '',
                        'v_25': '', 'v_50': '', 'v_75': '',
                        'v_100': '', 'v_99999': '' },
               }
    
    # initialize sort form lists
    context['orderby_select'][request.session['sort_order']['orderby']] = 'selected="selected"'
    context['limit_select']['v_' + str(request.session['sort_order']['limit'])] = 'selected="selected"'
    
    # content data
    
    # sort products
    def sortFunction(obj):
        return obj.__getattribute__(request.session['sort_order']['orderby'])
    
    reverse_type = request.session['sort_order']['order_type'] == 'desc'

    sortedProducts = sorted(resultSet, key=sortFunction, reverse=reverse_type)
    
    # new paginator
    paginator = Paginator(sortedProducts, request.session['sort_order']['limit'])
    
    pages_range = tuple(n + 1 for n in range(paginator.num_pages))
    print pages_range
    try:
        if not (int(page) in pages_range):
            raise Http404
    except:
        raise Http404   
    
    context['product_class_info'] = product_class
    context['page_name'] = 'productsAll_transition' if product_class is None else 'product_class_transition'
    context['object_list'] = paginator.page(int(page)).object_list
    context['page_number'] = int(page)
    context['page_surround'] = {'previous': int(page)-1,
                                  'next': 'none' if int(page) == paginator.num_pages else int(page)+1
                                }
    context['pages_range'] = pages_range
    
    # last part
    template = 'products.html'
    return render(request, template, context)
  
  
def product(request, pk):

    if handle_basket_query(request):
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    try:
        this_product = get_object_or_404(Product, id=int(pk), accepted=True)
    except:
        messages.error(request, '%s is not a valid product id number!' % (pk))
        raise Http404
    
    # Handle order for adding to the backet
    
    if request.method == 'POST' and request.POST.get('form_name') == 'product':
            
        try:
            quantity=int(request.POST.get('quantity'))
            
        except:
            messages.error(request, 'Quantity field has incorrect value.')
        
        if quantity < 1:
            messages.error(request, 'Quantity field must be positive number.')
        
        
        if not request.session.get('basket_products'):
            request.session['basket_products'] = []
        
        basket_products = request.session.get('basket_products')    
        
        # check if we already have same orderded products
        search_list = [(d['product_id'], d['size'], d['color']) for d in request.session['basket_products']]
        needed_tuple = this_product.id, request.POST.get('size', None), request.POST.get('color', None)
        
        if needed_tuple in search_list:
            needed_product = basket_products[search_list.index(needed_tuple)]
            
            needed_product['quantity'] += quantity
            needed_product['price'] += float(quantity * this_product.price)
            # do the apdate
        else:
            # create new temporary product
            basket_products.append({'product_id': this_product.id,
                                    'size': request.POST.get('size', None),
                                    'color': request.POST.get('color', None),
                                    'quantity': quantity,
                                    'price': float(quantity * this_product.price)})
        # save changesin session
        request.session.modified = True
        
        messages.info(request, 'Added to a basket %s, quantity: %d.' %
                      (unicode(this_product), quantity))
        
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    # Rewiew form
    
    if request.method == 'POST' and request.POST.get('form_name') == 'review':
        # create a form instance and populate it with data from the request:
        review_form = ReviewForm(request.POST)
        # check whether it's valid:
        
        if review_form.is_valid():
            # create new review
            Review.objects.create(
                title = review_form.cleaned_data['title'],
                text = review_form.cleaned_data['text'],
                
                name = review_form.cleaned_data['name'],
                email = review_form.cleaned_data['email'],
                author_hided = review_form.cleaned_data['author_hided'],
                product_id = this_product.id
            )
            
            messages.success(request, 'Your review is accepted!')

            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    else:
        review_form = ReviewForm(initial=dict((k, '') for k in ReviewForm().fields.keys()))
    
    # Form our context
    context = {
        'object': this_product,
        'images': Product_image.objects.filter(product_id = this_product),
        'product_sizes': this_product.product_size.all(),
        'product_colors': this_product.product_color.all(),
        'basket_products': get_basket_products(request),
        'badges_info': get_badges_info(request),
        'review_form': review_form,
        'review_list': Review.objects.filter(product_id = this_product.id, accepted = True)
        }
    
    template = 'product.html'
    return render(request, template, context)

def order(request):
    
    # backet
    if handle_basket_query(request):
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    #============================
    
    if request.method == 'POST' and request.POST.get('form_name') == 'order':
        
        # create a form instance and populate it with data from the request:
        form = OrderForm(request.POST)
        # check whether it's valid:
        
        have_products = bool(request.session.get('basket_products'))
        if not have_products:
            messages.error(request, u'Your basket is empty. Please, order first.')
            
        if form.is_valid() and have_products:
            
            # DB activity
            
            # check by e-mail,
            # if we have this customer, append/rewrite his data
            # if havan't, create new one
            try:
                customer = Customer.objects.get(email=form.cleaned_data['email'])
                
                additional_name = form.cleaned_data.get('name')
                
                if not customer.name:
                    customer.name = additional_name
                    
                elif additional_name and not additional_name in customer.name:
                    customer.name = "%s, %s" % (customer.name, additional_name)
                
            except:
                customer = Customer.objects.create(email = form.cleaned_data.get('email'),
                                    name = form.cleaned_data.get('name') )
            # update new one
            if form.cleaned_data.get('bosoms'): customer.bosoms = int(form.cleaned_data.get('bosoms'))
            if form.cleaned_data.get('grouth'): customer.grouth = int(form.cleaned_data.get('grouth'))
            if form.cleaned_data.get('hips'): customer.hips = int(form.cleaned_data.get('hips'))
            
            customer.save()
    
            # create and bind an address to customer
            if form.cleaned_data.get('city') or form.cleaned_data.get('address')\
                or form.cleaned_data.get('phone') or form.cleaned_data.get('fax'):
               
                Address.objects.get_or_create(customer_id=customer.id,
                                    city = form.cleaned_data.get('city'),
                                    address = form.cleaned_data.get('address'),
                                    phone = int(form.cleaned_data.get('phone')) if form.cleaned_data.get('phone') else None,
                                    fax = int(form.cleaned_data.get('fax')) if form.cleaned_data.get('fax') else None )

             
            # create new purchase order
     
            new_order = Purchase_order.objects.create(customer_id=customer.id,
                                    delivery = form.cleaned_data.get('delivery'),
                                    payment = form.cleaned_data.get('payment'),
                                    note = form.cleaned_data.get('note'),
                                    price = 0 )
            
            # handle basket products
            products_list = []
            for product in request.session['basket_products']:
                new_order.price += product['price']
                ordered_product = Ordered_product.objects.create(
                                    order_id = new_order.id,
                                    product_id = get_object_or_404(Product, id=product['product_id']).id,
                                    size_id = get_object_or_404(Product_size, name=product['size']).id if product['size'] else None,
                                    color_id = get_object_or_404(Product_color, name=product['color']).id if product['color'] else None,
                                    quantity = product['quantity'],
                                    price = Decimal(str(product['price']))
                )
                
                products_list.append(get_object_or_404(Product, id=product['product_id']).name)
            
            new_order.price = Decimal(str(new_order.price))
            new_order.save()
     
            messages.success(request, u'Order %s was created. products: %s' %
                              (new_order, '; '.join(products_list) ) )
                
            del request.session['basket_products']
            
            # save changesin session
            request.session.modified = True
           
            return HttpResponseRedirect(request.META['HTTP_REFERER'])

    else:
        form = OrderForm(initial=dict((k, '') for k in OrderForm().fields.keys()))
    
    context = { 'form': form,
                'basket_products': get_basket_products(request),
                'badges_info': get_badges_info(request) }
    
    template = 'order.html'
    
    return render(request, template, context)


def basket(request):

    if handle_basket_query(request):
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    context = {'basket_products': get_basket_products(request),
                'badges_info': get_badges_info(request) }
    
    template = 'basket.html'
    return render(request, template, context)
    