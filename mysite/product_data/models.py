from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=250)
    def __unicode__(self):
        return u"%s" % (self.name)
     
class Retailer(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(max_length=1000, null=True, blank=True)
    code = models.CharField(max_length=3, primary_key=True, default='unk')
    description = models.CharField(max_length=10000, null=True, blank=True)
    def __unicode__(self):
        return u"%s" % (self.code)
    
class Brand(models.Model):
    name = models.CharField(max_length=250, primary_key=True)
    def __unicode__(self):
        return u"%s" % (self.name)

class Product(models.Model):
    retailer = models.ForeignKey(Retailer)
    brand = models.ForeignKey(Brand)
    category = models.ForeignKey(Category)
    price = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True) #change
    msrp = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    date_of_fetch = models.DateTimeField()
    site_pid = models.CharField(max_length=1000, primary_key=True)
    url = models.URLField(max_length=1000)
    reviews = models.CharField(max_length=10000, null=True, blank=True)
    image_url = models.URLField(max_length=1000, null=True, blank=True)
    title = models.CharField(max_length=500)
    size = models.CharField(max_length=500, null=True, blank=True)
    country = models.CharField(max_length=150, null=True, blank=True)
    color = models.CharField(max_length=500, null=True, blank=True)
    description = models.CharField(max_length=10000, null=True, blank=True)
    meta_keywords = models.CharField(max_length=500, null=True, blank=True)
    meta_title = models.CharField(max_length=500, null=True, blank=True)
    meta_description = models.CharField(max_length=750, null=True, blank=True)
    rel_canon = models.URLField(max_length=1000, null=True, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    def __unicode__(self):
        return u"%s (%s)" % (self.title, self.site_pid)
    
    
    
    
    #authors = models.ManyToManyField(Author)
    #publisher = models.ForeignKey(Publisher)
    #publication_date = models.DateField()