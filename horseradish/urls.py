from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from horseradish.views import HelpView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^help/$', login_required(HelpView.as_view()), name='horseradish.help'),
    url(r'^search/', include('haystack.urls')),
    url(r'^', include('googleauth.urls')),
    url(r'^', include('photolib.urls')),
)
