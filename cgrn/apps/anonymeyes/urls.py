from django.conf.urls import patterns, include, url
from apps.anonymeyes.views import *

urlpatterns = patterns('apps.anonymeyes.views',
                       url(r'^$', IndexView.as_view(), name='index'),
                       url(r'^contact/$', ContactView.as_view(), name='contact'),
                       url(r'^thanks/$', ThanksView.as_view(), name='thanks'),
                       url(r'^about/$', AboutView.as_view(), name='about'),
                       url(r'^help/$', HelpView.as_view(), name='help'),
                       url(r'^list/$', PatientListView.as_view(), name='list'),
                       url(r'^detail/(?P<pk>\d+)/$', PatientDetailView.as_view(), name='detail'),
                       url(r'^delete/(?P<pk>\d+)/$', PatientDeleteView.as_view(), name='delete'),
                       url(r'^create/$', PatientCreateView.as_view(), name='create'),
                       url(r'^update/(?P<pk>\d+)/$', PatientUpdateView.as_view(), name='update'),
                       url(r'^wizard/(?P<step>.+)/$', 'wizard', name='wizard_step'),
                       url(r'^wizard/$', 'wizard', name='wizard'),
                       url(r'^visualacuityreadings/(?P<scale_pk>\d+)/$', VisualAcuityReadingsView.as_view()),
                       url(r'^visualacuityscales/(?P<method_pk>\d+)/$', VisualAcuityScalesView.as_view()),
                       url(r'^diagnoses/(?P<pk>\d+)/$', DiagnosesView.as_view()),
                       url(r'^uuid/(?P<uuid>.+)/$', PatientUUIDView.as_view()),
                       url(r'^profile/$', ProfileDetailView.as_view(), name='profile_detail'),
                       url(r'^profile/update/$', ProfileUpdateView.as_view(), name='profile_update'),
)
