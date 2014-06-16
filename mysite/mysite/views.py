from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.template import Context
from django.http import HttpResponse
import datetime
import MySQLdb
from product_data.models import *


def getResults(hcpcs, state):
  db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="", # your password
                      db="doctors") # name of the data base

  cur = db.cursor() 

  # Use all the SQL you like
  cur.execute("SELECT npi,first_name, last_name, num_services, hcpcs_description, city, state FROM medicare where hcpcs_code='" + hcpcs + "' and state = '" + state + "' ORDER BY num_services DESC LIMIT 10")

  # print all the first cell of all the rows
  
  rows = cur.fetchall()
  cur.close()
  return rows

def search(request):
    if 'hcpcs' in request.GET and 'state' in request.GET:
        if 'hcpcs' in request.GET and request.GET['hcpcs']:
            hcpcs = request.GET['hcpcs']
            state = request.GET['state']
            results = getResults(hcpcs, state)
            print results
            #products = Product.objects.filter(description__icontains=q)
            #print products[1].brand
            #print len(products)
        #if 'brand' in request.GET and request.GET['brand']:
         #   brand = request.GET['brand']
          #  products = Product.objects.filter(title__icontains=brand)
        #if 'title' in request.GET and request.GET['title']:
         #   title = request.GET['title']
          #  products = Product.objects.filter(title__icontains=title)
        if 'sort_by' in request.GET and request.GET['sort_by']:
            sort_by = request.GET['sort_by']
            if sort_by == 'discount':
                products = products.extra(select={ 'd_field' : '((1 - price/msrp)*100)' }).extra(order_by=['d_field'])
            else:
                products = products.order_by('-'+sort_by)  
        return render_to_response('search_results.html',
            {'products': results
             #'query': q
             })
    else:
        error = "Welcome"
        return render_to_response('search_form.html',
                                  {'error':error})


def hello(request):
	return HttpResponse("Hello world")
#
#def current_datetime(request):
#	now = datetime.datetime.now()
#	t = get_template('current_datetime.html')
#	html = t.render(Context({'current_date':now}))
#	return HttpResponse(html)
#
#def hours_ahead(request, offset):
#	try:
#		offset = int(offset)
#	except ValueError:
#		raise Http404()
#	dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
#	assert False
#	html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
#	return HttpResponse(html)
