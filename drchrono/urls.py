from django.conf.urls import include, url
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

from drchrono import views


urlpatterns = [
    url(r'^setup/$', views.SetupView.as_view(), name='setup'),
    url(r'^welcome/$', views.DoctorSchedule.as_view(), name='welcome'), #name was originally setup
    url(r'^kiosk/$', views.Kiosk.as_view(), name='kiosk'),
    url(r'^kiosk/patientCheckIn$', views.CheckinView.as_view(), name='patientCheckIn'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
]