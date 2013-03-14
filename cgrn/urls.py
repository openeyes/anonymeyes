from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url="anonymeyes")),
    url(r'^anonymeyes/', include('apps.anonymeyes.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name = 'accounts_login'),
    url(r'^accounts/profile/$', RedirectView.as_view(url="/anonymeyes/profile/")),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name = 'accounts_logout'),
    url(r'^admin/password_reset/$', 'django.contrib.auth.views.password_reset', name='admin_password_reset'),
    url(r'^admin/password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    url(r'^admin/', include(admin.site.urls)),

)
