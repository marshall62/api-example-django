"""
WSGI config for drchrono project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os, sys

# these changes come from
# https://stackoverflow.com/questions/14927345/importerror-no-module-named-django-core-wsgi-apache-virtualenv-aws-wsgi
# add the hellodjango project path into the sys.path
# they are here to get around an error that comes up when running with apache2
# ImportError: No module named django.core.wsgi
sys.path.append('/srv/raiddisk/dev/pydev/drc2/drchrono')

# add the virtualenv site-packages path to the sys.path
sys.path.append('/srv/raiddisk/dev/pydev/drc2/venv/lib/python3.5/site-packages')

# end changes

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drchrono.settings")

# turn on https per instructions at https://www.pdxpixel.com/blog/2014/02/04/setting-up-django-site-ssl-apache-mod_wsgi-mod_ssl/
# settings.py changed also
os.environ['HTTPS'] = "on"


from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
