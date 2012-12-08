import collections
import urllib2
from lxml import etree
from lxml.html import parse
from math import *
import re
import os
import datetime
from random import randint
from time import sleep
import csv
from mysite.settings import *
from product_data.models import *
from bs4 import BeautifulSoup
from os.path import isfile, getsize


import logging
with open('productFetch.log', 'w'):	#clear logging file
    pass
logging.basicConfig(filename='productFetch.log',level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.debug('This message should go to the log file')

def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)


def counter(object):
    pass

counter.tried_seeds, counter.tired_product_urls, counter.new_parsed_urls, counter.success_products = 0, 0, 0, 0
path_saved_requests = "temp/"

list_of_cols = ['retailer_code',		
				'brand',
				'category',
				'price',
				'msrp',
				'date_of_fetch',
				'site_pid',
				'url',
				'reviews',
				'image_url',
				'title',
				'size',
				'country',
				'color',
				'description',
				'meta_keywords',
				'meta_title',
				'meta_description',
				'rel_canon']

class Product_ob(object):
	def __init__(self, p_data):
		self.retailer_code = p_data['retailer_code']
		self.brand = p_data['brand']
		self.category = p_data['category']
		self.current_price = p_data['price']
		self.msrp = p_data['msrp']
		self.date_of_fetch = p_data['date_of_fetch']
		self.site_pid = p_data['site_pid']
		self.url = p_data['url']
		self.reviews = p_data['reviews']
		self.image_url = p_data['image_url']
		self.title = p_data['title']
		self.size = p_data['size']
		self.country = p_data['country']
		self.color = p_data['color']
		self.description = p_data['description']
		self.meta_title = p_data['meta_title']
		self.meta_keywords = p_data['meta_keywords']
		self.meta_description = p_data['meta_description']
		self.rel_canon = p_data['rel_canon']
	
	def refresh(self):
		pass
	
	def create_dict(self):
		data = [self.retailer_code,
				self.brand,
				self.category,
				self.current_price,
				self.msrp,
				self.date_of_fetch,
				self.site_pid,
				self.url,
				self.reviews,
				self.image_url,
				self.title,
				self.size,
				self.country,
				self.color,
				self.description,
				self.meta_title,
				self.meta_keywords,
				self.meta_description,
				self.rel_canon]

		dictionary = dict(zip(list_of_cols,data))
		return dictionary
	
	def __str__(self):
		key_val_dict = self.create_dict()
		result = ''
		for key in key_val_dict:
			result += "%s='%s', " % (key, key_val_dict[key])
		return result

class Utilities(object):
	def __init__(self):
		pass

	def clean(self, obj):
		return obj.encode('ascii', 'ignore').strip().replace("'", '').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
	
	def clean_num(self, obj):
		obj = self.clean(obj)
		obj = obj.replace('$', '').replace(',', '')
		return float(obj)

	def save_file(self, data, f_name):
		with open(f_name, 'w') as f:
			f.write(str(data))
			
	def category_finder(self, title, description):
		return 'unk'
	
	#fetches files
	
	def product_request(self, fname, product_url):	
	    n = 0
	    while (n < 1):
		try:
		    print 'Try reading file ...'
		    fsize = getsize(fname)
		    if (fsize < 100):
			os.remove(f)
			break
		    doc = parse(fname).getroot()
		    print "Used saved file"
		    n=1
		except:
		    print "Using internet ..."
		    req = urllib2.Request(product_url)
		    req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4")
		    read_product_url = urllib2.urlopen(product_url)
		    sleep(randint(10,100)/10)
		    self.save_file(read_product_url.read(), fname)
		    counter.new_parsed_urls += 1
	    return doc

		
util = Utilities()
	

#For Nordstrom unction takes product_URL, and parses relevant data, returns a dictionary for the product
def prod_fetch_nordstrom(product_url):
	print product_url
	retailer_code = "NRD"
	doc = ''
	
	# finds the pid of a URL
	def find_pid(product_url):
		pid = {}
		try:
			pid = re.search('''/\d+\?''', product_url)
			print pid, 'found'
			pid = pid.group(0)
			pid = pid.replace('/', '').replace('?', '')
		except:
			print "did not find PID in URL"
			pid = "unknown_pid"
		return pid
	pid = find_pid(product_url)
	fname = path_saved_requests + retailer_code + pid + ".txt"
	doc = util.product_request(fname, product_url)
	
	#Parses data
	meta_title, meta_keywords, meta_description, rel_canon = '', '', '', ''
	
	try:
	    raw_msrp = doc.xpath('//span[@class="price regular"]/text()')[0]
	    raw_msrp = raw_msrp.replace('Was: ','')
	    msrp =	util.clean_num(raw_msrp)
	    print msrp
	except:
	    msrp = .01
	    print "no msrp found"
	
	try:
	    raw_price = doc.xpath('//span[@class="price sale"]/text()')[0]
	    raw_price = raw_price.replace('Now: ','')
	    price =	util.clean_num(raw_price)
	    print price
	except:
	    print "no sale price found"
	    price = msrp
	

	
	date_of_fetch = modification_date(fname)
	
	for a in doc.xpath('//div[@class="fashion-photo-wrapper"]//img'):
		image_url = a.get('src')
		print image_url
	
	
	for a in doc.xpath('//h1/text()'):
		if (a.strip()):
			title = util.clean(a)
			print title
	
	brand = ''
	
	for a in doc.xpath('//div[@class="brand-content"]//ul//li//a/text()'):
	    print a
	    brand = util.clean(a)
	
	if brand == '':
	    brand = title.split()[0]
	    print brand
	
	
	for a in  doc.xpath('//meta[@name="title"]'):
		meta_title = util.clean(a.get('content'))
		print meta_title
		
	for a in doc.xpath('//meta[@name="description"]'):
		meta_description = a.get('content')
	meta_description = util.clean(meta_description)
	print meta_description

		
	for a in doc.xpath('//meta[@name="keywords"]'):
		meta_keywords = util.clean(a.get('content'))
		print meta_keywords
		
	for a in doc.xpath('//link[@rel="canonical"]'):
		rel_canon = a.get('href')
		print "END REL"
		print rel_canon
		print "START REL"
	
	description = ''
	for a in doc.xpath('//div[@class="content"]//text()'):
		if (a.strip()):
			description += util.clean(a)
	print "START DESC"
	print description
	print "END DESC"

	# find sizes and colors
	arr = []
	size = []
	color = []
	
	for a in doc.xpath("//label/../..//li//label//text()"):
	    print a
	    color.append(a)
	
	for a in doc.xpath("//label/../..//a//label//text()"):
	    print a
	    size.append(a)
	    
	    
	if color==[]:
	    color='null';
	if size==[]:
	    size='null'

	print size
	print color
	
	country = ''
	reviews = ''
	
	p_data = {}
	p_data['retailer_code'] = retailer_code
	p_data['brand'] = brand
	p_data['category'] = util.category_finder(title, description)
	p_data['price'] = price
	p_data['msrp'] = msrp
	p_data['date_of_fetch'] = date_of_fetch
	p_data['site_pid'] = retailer_code + pid
	p_data['url'] = product_url
	p_data['reviews'] = reviews
	p_data['image_url'] = image_url
	p_data['title'] = title
	p_data['size'] = str(size)
	p_data['country'] = country
	p_data['color'] = str(color)
	p_data['description'] = description
	p_data['meta_title'] = meta_title
	p_data['meta_keywords'] = meta_keywords
	p_data['meta_description'] = meta_description
	p_data['rel_canon'] = rel_canon
	p_data['discount'] = (msrp - price)/msrp*100
	return p_data



#For NM unction takes product_URL, and parses relevant data, returns a dictionary for the product
def prod_fetch_nm(product_url):
	print product_url
	retailer_code = "NM"
	doc = ''
	
	# finds the pid of a URL
	def find_pid(product_url):
		pid = {}
		try:
			pid = re.search('''prod[0-9]*''', product_url)
			print pid, 'found'
			pid = pid.group(0)
			pid = pid.replace('ItemId=', '')
		except:
			print "did not find PID in URL"
			pid = "unknown_pid"
		return pid
	pid = find_pid(product_url)
	fname = path_saved_requests + retailer_code + pid + ".txt"
	doc = util.product_request(fname, product_url)
	
	#Parses data
	meta_title, meta_keywords, meta_description, rel_canon = '', '', '', ''
	
	try:
	    raw_msrp = doc.xpath('//div[@class="price pos2"]/text()')[0]
	    msrp =	util.clean_num(raw_msrp)
	    print msrp
	except:
	    msrp = .01
	    print "no msrp found"
	
	try:
	    raw_price = doc.xpath('//div[@class="price pos1"]/text()')[0]
	    price =	util.clean_num(raw_price)
	    print price
	except:
	    print "no sale price found"
	    price = msrp
	

	
	date_of_fetch = modification_date(fname)
	
	for a in doc.xpath('//div[@class="img-wrap"]//img'):
		image_url = a.get('src')
	
	for a in doc.xpath('//span[@class="designer"]/text()'):
		brand = util.clean(a)
	if (brand == ''):
		for a in doc.xpath('//span[@class="designer"]//a/text()'):
			brand = util.clean(a)

	for a in doc.xpath('//h1/text()'):
		if (a.strip()):
			title = util.clean(a)
	
	for a in  doc.xpath('//meta[@name="title"]'):
		meta_title = util.clean(a.get('content'))
		
	for a in doc.xpath('//meta[@name="description"]'):
		meta_description = a.get('content')
	meta_description = util.clean(meta_description)

		
	for a in doc.xpath('//meta[@name="keywords"]'):
		meta_keywords = util.clean(a.get('content'))
		
	for a in doc.xpath('//link[@rel="canonical"]'):
		rel_canon = a.get('href')
	
	description = ''
	for a in doc.xpath('//div[@class="cutline short"]//div//div//text()'):
		print a
		if (a.strip()):
			description += util.clean(a)
	print description

	# find sizes and colors
	size = []
	color = []
	for a in doc.xpath('//script/text()'):
		if pid+'Matrix' in a:
			regexp = re.compile('''new product(?:.)*;''')
			t = 1
			for match in re.findall(regexp, a):
				size_match = util.clean(match.split(',')[3])
				size.append(size_match)
				color_match = match.split(',')[4]
				color_match = util.clean(color_match)
				color.append(color_match)
	if color == ['null']:
		color = size
		size = 'null'
	print size
	print color
	country = ''
	reviews = ''
	
	p_data = {}
	p_data['retailer_code'] = retailer_code
	p_data['brand'] = brand
	p_data['category'] = util.category_finder(title, description)
	p_data['price'] = price
	p_data['msrp'] = msrp
	p_data['date_of_fetch'] = date_of_fetch
	p_data['site_pid'] = retailer_code + pid
	p_data['url'] = product_url
	p_data['reviews'] = reviews
	p_data['image_url'] = image_url
	p_data['title'] = title
	p_data['size'] = str(size)
	p_data['country'] = country
	p_data['color'] = str(color)
	p_data['description'] = description
	p_data['meta_title'] = meta_title
	p_data['meta_keywords'] = meta_keywords
	p_data['meta_description'] = meta_description
	p_data['rel_canon'] = rel_canon
	p_data['discount'] = (msrp - price)/msrp*100
	return p_data

#For HugoBoss function takes product_URL, and parses relevant data, returns a dictionary for the product
def prod_fetch_hb(product_url):
	#uses beautiful soup to parse
	print product_url
	retailer_code = "HB"
	doc = ''
	
	# finds the pid of a URL
	def find_pid(product_url):
		pid = {}
		try:
			pid = re.search('''hbna[0-9]*''', product_url)
			print pid, 'found'
			pid = pid.group(0)
			pid = pid.replace('', '')
		except:
			print "did not find PID in URL"
			pid = "unknown_pid"
		return pid
	pid = find_pid(product_url)
	fname = path_saved_requests + retailer_code + pid + ".txt"
	doc = util.product_request(fname, product_url)
	
	#Parses data
	meta_title, meta_keywords, meta_description, rel_canon = '', '', '', ''
	
	
	with open(fname, 'r') as f:
	    html_doc = f.read()
	soup = BeautifulSoup(html_doc, "xml")
	
	raw_msrp = soup.find("div", class_="standardprice").string
	msrp =	util.clean_num(raw_msrp)
	print msrp
	
	try:
	    raw_price = soup.find("div", class_="salesprice issalesprice").string
	    price =	util.clean_num(raw_price)
	    print price
	except:
	    price = msrp   
	
	date_of_fetch = modification_date(fname)
	
	
	image_url = soup.find("img", class_="mainImage")['src']
	brand = util.clean(soup.find("div", class_="productinfo").img['title'])
	title = util.clean(soup.title.string)
	
	
	for a in  doc.xpath('//meta[@name="title"]'):
		meta_title = util.clean(a.get('content'))
		
	for a in doc.xpath('//meta[@name="description"]'):
		meta_description = a.get('content')
	meta_description = util.clean(meta_description)

		
	for a in doc.xpath('//meta[@name="keywords"]'):
		meta_keywords = util.clean(a.get('content'))
		
	for a in doc.xpath('//link[@rel="canonical"]'):
		rel_canon = a.get('href')
	
	description = soup.find("body").p.string
	description = util.clean(description)
	print description

	# find sizes and colors
	
	size = []
	color = []
	found = soup.find("select", class_="size formidable-ajust-widths")
	found2 = found.find_all("option")
	for f in found:
	    f = util.clean(f.string)
	    if len(f) >> 0:
		size.append(f)
	    
	found = soup.find_all('a', class_='swatchanchor')
	for f in found:
	    f = util.clean(f.string)
	    color.append(f)
	
	print size
	print color
	country = ''
	reviews = ''
	
	p_data = {}
	p_data['retailer_code'] = retailer_code
	p_data['brand'] = brand
	p_data['category'] = util.category_finder(title, description)
	p_data['price'] = price
	p_data['msrp'] = msrp
	p_data['date_of_fetch'] = date_of_fetch
	p_data['site_pid'] = retailer_code + pid
	p_data['url'] = product_url
	p_data['reviews'] = reviews
	p_data['image_url'] = image_url
	p_data['title'] = title
	p_data['size'] = str(size)
	p_data['country'] = country
	p_data['color'] = str(color)
	p_data['description'] = description
	p_data['meta_title'] = meta_title
	p_data['meta_keywords'] = meta_keywords
	p_data['meta_description'] = meta_description
	p_data['rel_canon'] = rel_canon
	p_data['discount'] = (msrp - price)/msrp*100
	return p_data
	
	
	
	
list_of_product_urls = []



crawler_seed = ["""http://shop.nordstrom.com/c/all-mens-sale?page=1"""
		#"""http://www.neimanmarcus.com/etemplate/et1.jsp?itemId=cat980731&N=4294914706&siloId=cat980731&pageSize=99999""",
		#"""http://www.neimanmarcus.com/etemplate/et1.jsp?tv=lc&N=4294914706&st=s&pageSize=99999""",
		#"""http://store-us.hugoboss.com/sale/mens-clothing-and-accessories/71234,en_US,sc.html?sz=120""",
		#"""http://store-us.hugoboss.com/sale/mens-clothing-and-accessories/71234,en_US,sc.html?start=120&sz=120""",
		#"""http://store-us.hugoboss.com/sale/mens-clothing-and-accessories/71234,en_US,sc.html?start=240&sz=120""",
		#"""http://store-us.hugoboss.com/sale/mens-clothing-and-accessories/71234,en_US,sc.html?start=3600&sz=120""",
		#"""http://store-us.hugoboss.com/sale/mens-clothing-and-accessories/71234,en_US,sc.html?start=480&sz=120""",
		#"""http://store-us.hugoboss.com/sale/mens-clothing-and-accessories/71234,en_US,sc.html?start=600&sz=120""",
		]

counter.tried_seeds = len(crawler_seed)


for cat_page in crawler_seed:
    if 'www.neimanmarcus' in cat_page:
	rel_url = """http://www.neimanmarcus.com"""
	doc = parse(cat_page).getroot()
	for a in doc.xpath('//div[@class="productdesigner"]//a'):
	    list_of_product_urls.append(rel_url + a.get('href'))
    if 'hugoboss.com' in cat_page:
	print cat_page
	print "found"
	rel_url = """http://store-us.hugoboss.com/"""
	doc = parse(cat_page).getroot()
	for a in doc.xpath('//div[@class="productimage"]//a'):
	    print a.get('href')
	    list_of_product_urls.append(rel_url + a.get('href'))
    if 'nordstrom.com' in cat_page:
	for i in range(1,6):
	    len_list = len(list_of_product_urls)
	    cat_page_each = re.sub("page=1", "page="+str(i), cat_page)
	    print cat_page_each
	    rel_url = """http://shop.nordstrom.com"""
	    doc = parse(cat_page_each).getroot()
	    print doc
	    
	    #read_product_url = urllib2.urlopen(cat_page_each)
	    #read_doc = read_product_url.read()
	    #print read_doc.split('div')[1:5]
	    #
	    #print '\n\n\n\n\n\n\n\n\n\n\n\n'
	    #for a in  doc.xpath('//meta[@name="title"]'):
		#print a.get('content')
		#meta_title = util.clean(a.get('content'))
    		#print meta_title
	    for a in doc.xpath('//div[@class="info new-markdown men adult"]//a'):
		list_of_product_urls.append(rel_url + a.get('href'))
	    for a in doc.xpath('//div[@class="info default men adult"]//a'):
		list_of_product_urls.append(rel_url + a.get('href'))
	    if len_list == len(list_of_product_urls):
		break

print list_of_product_urls

for product_url in list_of_product_urls:
	counter.tired_product_urls += 1
	if 'neimanmarcus.com' in product_url:
	    try:
		p_data = prod_fetch_nm(product_url)
	    except:
		print "xxxxxxxxxxxxxxxxxxFAILED for: " + product_url
	elif 'hugoboss.com' in product_url:
	    try:
		p_data = prod_fetch_hb(product_url)
	    except:
		print "xxxxxxxxxxxxxxxxxxFAILED for: " + product_url
	elif 'nordstrom.com' in product_url:
	    #try:
	    p_data = prod_fetch_nordstrom(product_url)
	    #except:
		#print "xxxxxxxxxxxxxxxxxxFAILED for: " + product_url	
	if p_data:
	    try:
		brandobj = Brand.objects.get(name=p_data['brand'])
		print "brand exists"
	    except:    
		b1 = Brand(name=p_data['brand'])
		b1.save()
	    try:
		retailer=Retailer.objects.get(code=p_data['retailer_code'])
		print "retailer exists"
	    except:    
		r1 = Retailer(code=p_data['retailer_code'])
		r1.save()
	    finally:
		print p_data['discount']
		p1 = Product(
		    category=Category.objects.get(name=p_data['category']),
		    meta_description=p_data['meta_description'],
		    meta_title=p_data['meta_title'],
		    meta_keywords=p_data['meta_keywords'],
		    description=p_data['description'],
		    title=p_data['title'],
		    url=product_url,
		    country=p_data['country'],
		    brand=Brand.objects.get(name=p_data['brand']),
		    retailer=Retailer.objects.get(code=p_data['retailer_code']),
		    reviews=p_data['reviews'],
		    color=p_data['color'],
		    image_url=p_data['image_url'],
		    rel_canon=p_data['rel_canon'],
		    date_of_fetch=p_data['date_of_fetch'],
		    site_pid=p_data['site_pid'],
		    price=p_data['price'],
		    msrp=p_data['msrp'],
		    size=p_data['size'],
		    discount=p_data['discount'],
		    )
		try:
		    p1.save()
		    counter.success_products += 1
		    print 'xxxxxxxx'
		except:
		    logging.warning('Product failed save %s' % product_url)
	else:
	    print "no p_data exists"

logging.debug('Tried to fetch %s seeds' % counter.tried_seeds)
logging.debug('Tried to fetch %s product_urls' % counter.tired_product_urls)
logging.debug('Created %s new product files saved' % counter.new_parsed_urls)
logging.debug('Saved %s files to pdb' % counter.success_products)

print 'Tried to fetch %s seeds' % counter.tried_seeds
print 'Tried to fetch %s product_urls' % counter.tired_product_urls
print 'Created %s new product files saved' % counter.new_parsed_urls
print 'Saved %s files to pdb' % counter.success_products
