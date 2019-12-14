from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

from drchrono import views
from drchrono.sched.ScheduleKeeper import get_appts, update_stat
import drchrono.webhook.process as mywebhook


urlpatterns = [
    url(r'^setup/$', views.SetupView.as_view(), name='setup'),
    url(r'^welcome/$', views.DoctorSchedule.as_view(), name='welcome'), #name was originally setup
    url(r'^kiosk/old$', views.Kiosk.as_view(), name='kioskold'),
    url(r'^webhook/update$', mywebhook.handle_update, name='webhook'),
    url(r'^kiosk/$', views.CheckinView.as_view(), name='kiosk'),
    url(r'^appointments/$', get_appts, name='getAppointments'),
    url(r'^appointments/(?P<appointment_id>\d+)$', update_stat, name='updateAppointments'),
    url(r'^kiosk/patientInfo/(?P<patient_id>\d+)$', views.PatientInfoView.as_view(), name='patientInfo'),
    url(r'^kiosk/checkout/(?P<patient_id>\d+)$', views.CheckoutSurveyView.as_view(), name='checkout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
]
