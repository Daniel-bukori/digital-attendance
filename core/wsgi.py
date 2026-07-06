"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()
# wsgi.py - Weka hii chini kabisa ya faili lililopo

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digital_attendance.settings')
application = get_wsgi_application()

# KODI YA KUDAREKI SUPERUSER KIOTOMATIKI ONLINE:
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    # Kagua kama admin yupo, kama hayapo mtengeneze
    if not User.objects.filter(username='admin').exists():
        # Hapa 'admin' ni username, na 'Admin@2026' ndio itakuwa password yako
        User.objects.create_superuser('admin', 'admin@iaa.ac.tz', 'Admin@2026')
        print("Superuser 'admin' ametengenezwa kikamilifu!")
except Exception as e:
    print("Error kwenye kutengeneza superuser:", e)
  
