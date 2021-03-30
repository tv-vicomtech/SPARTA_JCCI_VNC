import requests
import json
import httplib2, urllib
import traceback
from base64 import b64decode
from uuid import uuid4
from xml.etree import ElementTree

from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden
from django.conf import settings
from django.shortcuts import redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import resolve_url

from oauth2client.django_orm import Storage
from oauth2client.client import Credentials

from apiclient.discovery import build
import apiclient.errors
from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials

client_public_url = 'please fill in the public ip and port or url'
client_public_url = 'http://10.200.20.54'

client_id='4fd3db5e-8ac4-4d82-981f-5547f32fd5ee'
client_secret='75aacbc3-821b-48e1-9516-d7c30048f843'
redirect_uri = client_public_url + '/auth/keyrock_authenticate'
keyrock_url='https://jcci.sparta.eu:4443'

def is_authenticated(request):
    if not getattr(settings, 'EMAIL_ENFORCED'):
        return HttpResponse("Authentication not enforced")
        
    if request.user.is_authenticated():
        return HttpResponse(json.dumps({'user': str(request.user)}))
    return HttpResponseForbidden()

def get_redirect_host(request):
    try:
        http_host   = request.META['HTTP_X_FORWARDED_FOR']
        http_scheme = request.META['wsgi.url_scheme']
        redirect_uri = "%s://%s" % (http_scheme, http_host)
    except KeyError:
        redirect_uri = "/"
    return redirect_uri

def authenticate_with_keyrock(request):
    url = keyrock_url + '/oauth2/authorize?response_type=code&client_id=' + client_id + '&state=xyz&redirect_uri='+ redirect_uri 
    return HttpResponseRedirect(url)

def keyrock_authenticate_redirect(request):
    payload = {'client_id': client_id, 'client_secret': client_secret, 'code': request.GET['code'], 
        'redirect_uri': redirect_uri, 'grant_type': 'authorization_code'}
    r = requests.post(keyrock_url + "/oauth2/token", data=payload, verify=False)
    if r.status_code != 200:
        return HttpResponse("Could not authenticate")

    tokens = json.loads(r.text)
    id_tokens = tokens['access_token'].split('.')
    r = requests.get(keyrock_url + "/user?access_token=" + id_tokens[0] + "&action=GET&resource=VNC&app_id=" + client_id, verify=False)
    if ("Permit" in r.text):
        return redirect(get_redirect_host(request))
    else:
        return HttpResponse("not allowed")