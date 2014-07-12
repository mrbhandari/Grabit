from django.db import models

class Medicare(models.Model):
    npi = models.CharField(max_length=10, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    credentials = models.CharField(max_length=1000, null=True, blank=True) 
    gender = models.CharField(max_length=10, null=True, blank=True)
    entity_code = models.CharField(max_length=10, null=True, blank=True)
    street1 = models.CharField(max_length=1024, null=True, blank=True)
    street2 = models.CharField(max_length=1024, null=True, blank=True)
    city = models.CharField(max_length=1024, null=True, blank=True)
    zip_code = models.CharField(max_length=100, null=True, blank=True) #changed
    state = models.CharField(max_length=512, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    provider_type = models.CharField(max_length=1024, null=True, blank=True)
    medicare_indicator = models.CharField(max_length=2, null=True, blank=True)
    place_of_service = models.CharField(max_length=10, null=True, blank=True)
    hcpcs_code = models.CharField(max_length=100, null=True, blank=True)
    hcpcs_description = models.CharField(max_length=1024, null=True, blank=True)
    num_services = models.IntegerField(null=True, blank=True)
    num_uniq_users = models.IntegerField(null=True, blank=True)
    num_uniq_users_per_day = models.IntegerField(null=True, blank=True)
    avg_medicare_amt = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    std_dev_medicare_amt = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    avg_submitted_amt = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    std_dev_submitted_amt = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    avg_medicare_payment = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    std_dev_medicare_payment = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    
    def __unicode__(self):
        return u'%s %s %s' % (self.first_name, self.last_name, self.npi)
    



#
#class Category(models.Model):
#    name = models.CharField(max_length=250)
#    def __unicode__(self):
#        return u"%s" % (self.name)
#     
#class Retailer(models.Model):
#    name = models.CharField(max_length=100)
#    website = models.URLField(max_length=1000, null=True, blank=True)
#    code = models.CharField(max_length=3, primary_key=True, default='unk')
#    description = models.CharField(max_length=10000, null=True, blank=True)
#    def __unicode__(self):
#        return u"%s" % (self.code)
#    
#class Brand(models.Model):
#    name = models.CharField(max_length=250, primary_key=True)
#    def __unicode__(self):
#        return u"%s" % (self.name)
#
#class Product(models.Model):
#    retailer = models.ForeignKey(Retailer)
#    brand = models.ForeignKey(Brand)
#    category = models.ForeignKey(Category)
#    price = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True) #change
#    msrp = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
#    date_of_fetch = models.DateTimeField()
#    site_pid = models.CharField(max_length=1000, primary_key=True)
#    url = models.URLField(max_length=1000)
#    reviews = models.CharField(max_length=10000, null=True, blank=True)
#    image_url = models.URLField(max_length=1000, null=True, blank=True)
#    title = models.CharField(max_length=500)
#    size = models.CharField(max_length=500, null=True, blank=True)
#    country = models.CharField(max_length=150, null=True, blank=True)
#    color = models.CharField(max_length=500, null=True, blank=True)
#    description = models.CharField(max_length=10000, null=True, blank=True)
#    meta_keywords = models.CharField(max_length=500, null=True, blank=True)
#    meta_title = models.CharField(max_length=500, null=True, blank=True)
#    meta_description = models.CharField(max_length=750, null=True, blank=True)
#    rel_canon = models.URLField(max_length=1000, null=True, blank=True)
#    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
#    
#    def __unicode__(self):
#        return u"%s (%s)" % (self.title, self.site_pid)
#    

    
    #authors = models.ManyToManyField(Author)
    #publisher = models.ForeignKey(Publisher)
    #publication_date = models.DateField()