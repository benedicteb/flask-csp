#!/usr/bin/env python
import os
import json

from flask import make_response
from functools import wraps

class FlaskCSP(object):
    def __init__(self, defaults=None, app=None):
        if not defaults:
            defaults = {
                "script-src": "",
                "img-src": "",
                "child-src": "",
                "default-src": "'self'",
                "plugin-src": "",
                "style-src": "",
                "media-src": "",
                "object-src": "",
                "connect-src": "",
                "base-uri": "",
                "report-uri": "/csp_report"
            }

        self.defaults = defaults

        if app:
            app.after_request(self._set_csp_header)

    def _create_csp_string(self, cspDict):
        """
        create csp header string
        """
        policy = ['%s %s' % (k, v) for k, v in cspDict.items() if v != '']
        return '; '.join(policy)

    def _create_csp_headers(self, cspDict=None):
        if cspDict:
            csp = cspDict
        else:
            csp = self.defaults

        header_type = ''

        if 'report-only' in csp:
            if csp['report-only']:
                header_type = 'Content-Security-Policy-Report-Only'
            else:
                del csp['report-only']
        else:
            header_type = 'Content-Security-Policy'

        return {header_type: self._create_csp_string(csp)}

    def _set_csp_header(self, response):
        """
        Add CSP header to all requests.
        """
        headers = self._create_csp_headers()

        for header,value in headers.items():
            response.headers.setdefault(header, value)

        return response

    def update_defaults(self, cspDict):
        self.defaults = cspDict

    def csp_header(self, cspDict=None):
        """
        Decorator to include csp header on app.route wrapper
        """
        headers = self._create_csp_headers(cspDict)

        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                resp = make_response(f(*args, **kwargs))
                h = resp.headers
                for header, value in headers.items():
                    h[header] = value
                return resp
            return decorated_function
        return decorator
