from django.conf.urls import include, url
from drchrono.sched.Appointments import Appointments
from django.contrib import admin
admin.autodiscover()

from drchrono import views
from drchrono import data


urlpatterns = [
    url(r'^setup/$', views.SetupView.as_view(), name='setup'),
    url(r'^welcome/$', views.DoctorSchedule.as_view(), name='welcome'), #name was originally setup
    url(r'^kiosk/old$', views.Kiosk.as_view(), name='kioskold'),
    url(r'^kiosk/$', views.CheckinView.as_view(), name='kiosk'),
    url(r'^appointments/$', data.get_appointments, name='getAppointments'),
    url(r'^appointments/(?P<appointment_id>\d+)$', data.update_appointment_status, name='updateAppointments'),
    url(r'^kiosk/patientInfo/(?P<patient_id>\d+)$', views.PatientInfoView.as_view(), name='patientInfo'),
    url(r'^kiosk/checkout/(?P<patient_id>\d+)$', views.CheckoutSurveyView.as_view(), name='checkout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
]

# Stuff that needs to be done once at beginning
from drchrono.api_models.Doctor import Doctor
d = Doctor()
Appointments.set_doctor(d)

#TODO this runs while doing things like migrate.  Need to put a conditional in front of this so it only does it when running.

# gets all the doctors appointments and builds our local db PatientAppointment table.
# Appointments().load_all_appointments()


