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

def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

# fd = urllib2.urlopen(url)


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

		
util = Utilities()
	



#Function takes product_URL, and parses relevant data, returns a dictionary for the product
def prod_fetch(product_url):
	
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
	
	#fetches files
	fname = "temp/" + retailer_code + pid + ".txt"	
	print "Pid Found" + pid
	n = 0
	while (n < 1):
		try:

			print 'Try reading file ...'
			doc = parse(fname).getroot()
			print "Used saved file"
			n=1
		except:
			print "Using internet ..."
			req = urllib2.Request(product_url)
			req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4")
			read_product_url = urllib2.urlopen(product_url)
			sleep(randint(10,100)/10)
			util.save_file(read_product_url.read(), fname)

	#Parses data
	meta_title, meta_keywords, meta_description, rel_canon = '', '', '', ''

	raw_price = doc.xpath('//div[@class="price pos1"]/text()')[0]
	price =	util.clean_num(raw_price)
	print price
	
	raw_msrp = doc.xpath('//div[@class="price pos2"]/text()')[0]
	msrp =	util.clean_num(raw_msrp)
	print msrp
	
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
	return p_data

	
	
	
	
list_of_product_urls = []



crawler_seed = ["""http://www.neimanmarcus.com/etemplate/et1.jsp?N=4294966789&icid=src_Sale+Silo+Updated+Page""",
		   """http://www.neimanmarcus.com/etemplate/et1.jsp?N=4294966741&icid=src_Sale+Silo+Updated+Page""",
		   """http://www.neimanmarcus.com/etemplate/et1.jsp?N=4294966788&icid=src_Sale+Silo+Updated+Page""",
		   """http://www.neimanmarcus.com/etemplate/et1.jsp?No=0&viewClick=true&tv=lc&_requestid=30388&N=4294966789&pageSize=9999&viewClick=true""",
		   """http://www.neimanmarcus.com/etemplate/et1.jsp?No=120&tv=lc&_requestid=30388&N=4294966789"""
		   ]



for cat_page in crawler_seed:
	rel_url = """http://www.neimanmarcus.com"""
	doc = parse(cat_page).getroot()
	for a in doc.xpath('//div[@class="productdesigner"]//a'):
		list_of_product_urls.append(rel_url + a.get('href'))

print list_of_product_urls

fdata = ''




#f = open("test1.tsv", 'w')
#try:
#fieldnames = list_of_cols
#writer = csv.DictWriter(f, fieldnames=fieldnames, dialect='excel-tab')
#headers = dict( (n,n) for n in fieldnames )
#writer.writerow(headers)
for product_url in list_of_product_urls:
	#pdata =
	p_data = prod_fetch(product_url)
	try:
	    brandobj = Brand.objects.get(name=p_data['brand'])
	    print "brand exists"
	except:    
	    b1 = Brand(name=p_data['brand'])
	    b1.save()
	finally:
	    p1 = Product(
		category=Category.objects.get(name=p_data['category']),
		meta_description=p_data['meta_description'],
		meta_title=p_data['meta_title'],
		meta_keywords=p_data['meta_keywords'],
		description=p_data['description'],
		title=p_data['title'],
		url=product_url, country=p_data['country'],
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
		)
	    p1.save()
	    
	    #product = Product_ob(pdata)
	    #print product
	    #p1 = Product(product.__str__)
	    #p1.save()
	    print 'xxxxxxxx'
    #	writer.writerow(product.create_dict())
    #except:
    #	"DID NOT WORK"
    #finally:
    #    f.close()

