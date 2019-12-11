"""
WSGI config for drchrono project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drchrono.settings")

# turn on https per instructions at https://www.pdxpixel.com/blog/2014/02/04/setting-up-django-site-ssl-apache-mod_wsgi-mod_ssl/
# settings.py changed also
# os.environ['HTTPS'] = "on"

application = get_wsgi_application()
