from django.conf.urls import patterns, include, url
from anonymeyes.views import IndexView, PatientListView, PatientDetailView, PatientUpdateView, PatientCreateView

urlpatterns = patterns('anonymeyes.views',
                       url(r'^$', IndexView.as_view(), name='index'),
                       url(r'^list/$', PatientListView.as_view(), name='list'),
                       url(r'^detail/(?P<pk>\d+)/$', PatientDetailView.as_view(), name='detail'),
                       url(r'^create/$', PatientCreateView.as_view(), name='create'),
                       url(r'^update/(?P<pk>\d+)/$', PatientUpdateView.as_view(), name='update'),
                       url(r'^wizard/(?P<step>.+)/$', 'wizard', name='wizard_step'),
                       url(r'^wizard/$', 'wizard', name='wizard'),
)
