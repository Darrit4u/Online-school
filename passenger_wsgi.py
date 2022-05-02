# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u1666879/data/www/obshagana100.ru/')
sys.path.insert(1, '/var/www/u1666879/data/djangoenv/lib/python3.8/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'site_school.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()