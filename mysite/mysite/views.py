from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.template import Context
from django.http import HttpResponse
import datetime
from product_data.models import *



def search(request):
    if 'q' in request.GET or 'brand' in request.GET or 'title' in request.GET:
        if 'q' in request.GET and request.GET['q']:
            q = request.GET['q']
            print q
            products = Product.objects.filter(description__icontains=q)
            print products[1].brand
            print len(products)
        if 'brand' in request.GET and request.GET['brand']:
            brand = request.GET['brand']
            products = Product.objects.filter(title__icontains=brand)
        if 'title' in request.GET and request.GET['title']:
            title = request.GET['title']
            products = Product.objects.filter(title__icontains=title)
        if 'sort_by' in request.GET and request.GET['sort_by']:
            sort_by = request.GET['sort_by']
            if sort_by == 'discount':
                products = products.extra(select={ 'd_field' : '((1 - price/msrp)*100)' }).extra(order_by=['d_field'])
            else:
                products = products.order_by('-'+sort_by)  
        return render_to_response('search_results.html',
            {'products': products,
             #'query': q
             })
    else:
        error = "Please enter text in atleast one of the boxes below."
        return render_to_response('search_form.html',
                                  {'error':error})


def hello(request):
	return HttpResponse("Hello world")

def current_datetime(request):
	now = datetime.datetime.now()
	t = get_template('current_datetime.html')
	html = t.render(Context({'current_date':now}))
	return HttpResponse(html)

def hours_ahead(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
	dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
	assert False
	html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
	return HttpResponse(html)