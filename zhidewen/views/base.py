# -*- coding: utf-8 -*-

import json
from django import http


def JsonResponse(data):
    return http.HttpResponse(json.dumps(data), mimetype="application/json")


def response_json(view):
    def _view(*args, **kwargs):
        response = view(*args, **kwargs)
        if not isinstance(response, http.HttpResponse):
            response = JsonResponse(response)
        return response
    return _view


def success(data=None, msg=''):
    return JsonResponse({'success': True, 'msg': msg, 'data': data})


def error(msg='', data=None):
    return JsonResponse({'success': False, 'msg': msg, 'data': data})