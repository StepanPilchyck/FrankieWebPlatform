from django.shortcuts import render
import json
from django.http import HttpResponse
from weblayout.models import Language


def set_language(request, lang):

    if 'language' not in request.session:
        request.session['language'] = Language.objects.first().short_name
    request.session['language'] = lang

    serialized = json.dumps({'language': lang})
    return HttpResponse(serialized, content_type="application/json")


def get_language(request):

    if 'language' not in request.session:
        request.session['language'] = Language.objects.first().short_name

    return request.session['language']

