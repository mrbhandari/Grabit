from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from mysite.views import hello, search, hcpcs_autosuggest

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       (r'^$', search),
                       (r'^admin/', include(admin.site.urls)),
                       (r'^search/$', search),
                       (r'^hcpcs_autosuggest/$', hcpcs_autosuggest),
)

