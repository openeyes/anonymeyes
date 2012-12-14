from django.conf.urls import patterns, include, url

urlpatterns = patterns('anonymeyes.views',
                       url(r'^$', 'index'),
                       url(r'^create/(?P<step>.+)/$', 'create', name='create_step'),
                       url(r'^create/$', 'create', name='create'),
)
