from django.conf.urls import patterns, include, url
from anonymeyes.views import PatientWizard

urlpatterns = patterns('anonymeyes.views',
                       url(r'^$', 'index'),
                       url(r'^create/$', 'create'),
                       url(r'^thanks/$', 'thanks'),
)
