from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.template import Context
from django.http import HttpResponse
import datetime
import MySQLdb
from product_data.models import *
from django.utils import simplejson


def getResults(hcpcs, state):
  db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="thebakery", # your password
                      db="doctors") # name of the data base

  cur = db.cursor() 

  # Use all the SQL you like
  cur.execute("SELECT npi,first_name, last_name, num_services, hcpcs_description, city, state FROM medicare where hcpcs_code='" + hcpcs + "' and state = '" + state + "' ORDER BY num_services DESC LIMIT 100")

  # print all the first cell of all the rows
  
  rows = cur.fetchall()
  cur.close()
  return rows

def state_autosuggest(request):
    if 'term' in request.GET:
        search = request.GET['term']
        autores = [AK, AL, AR, AZ, CA, CO, CT, DC, DE, FL, GA, HI, IA, ID, IL, IN, KS, KY, LA, MA, MD, ME, MI, MN, MO, MS, MT, NC, ND, NE, NH, NJ, NM, NV, NY, OH, OK, OR, PA, RI, SC, SD, TN, TX, UT, VA, VT, WA, WI, WV, WY]
        return HttpResponse(simplejson.dumps(autores), mimetype='application/json')
    


def hcpcs_autosuggest(request):
    if 'term' in request.GET:
        search = request.GET['term']
        
        db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="thebakery", # your password
                      db="doctors") # name of the data base

        cur = db.cursor() 
      
        # Use all the SQL you like
        print "SELECT * FROM hcpcs_autosuggest where (hcpcs_code like '%" + search + "%' or hcpcs_description like '%" + search + "%') LIMIT 100;"
        cur.execute("SELECT * FROM hcpcs_autosuggest where (hcpcs_code like '%" + search + "%' or hcpcs_description like '%" + search + "%') LIMIT 100;")
        rows = cur.fetchall()
        cur.close()
        
        print len(rows)
        autores =[]
        i=0
        while i<len(rows):
            autores.append(rows[i][0] + " - " + rows[i][1])
            print i
            i = i +1
        print autores
        returndata = ["blue shoes", "red shoes"]
        
        # format what you return
        
        print search
        return HttpResponse(simplejson.dumps(autores), mimetype='application/json')
        #return render_to_response('search_form.html',
        #    {'hcpcs_autosuggest_results': rows
        #     })
        #

def search(request):
    if 'hcpcs' in request.GET and 'state' in request.GET:
        if 'hcpcs' in request.GET and request.GET['hcpcs']:
            hcpcs = request.GET['hcpcs']
            hcpcs = hcpcs.split(' -', 1)[0]
            print "DONE!!"
            print hcpcs
            state = request.GET['state']
            #providers = Medicare.objects.filter(hcpcs_code__icontains=hcpcs, state__icontains=state)
            #print providers[1].npi
            #print providers
            
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
        error = ""
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
