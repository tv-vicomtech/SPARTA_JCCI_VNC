from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import authentication as auth

urlpatterns = patterns('',
    url(r'^check/$', auth.is_authenticated, name='is_authenticated'),
    url(r'^keyrock/$', auth.authenticate_with_keyrock, name='keyrock'),
    url(r'^keyrock_authenticate/$', auth.keyrock_authenticate_redirect, name='keyrock_authenticate_redirect'),
)