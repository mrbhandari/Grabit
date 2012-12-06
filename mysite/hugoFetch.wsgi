import os
import sys

path = '/Grabit/mysite'
if path not in sys.path:
        sys.path.append('/Grabit/mysite')

import site

site.addsitedir('/project/hugoFetch/lib/python2.7/site-packages/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
                        
                                                                               