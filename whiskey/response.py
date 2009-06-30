from Cookie import SimpleCookie

class WSGIResponse(object):
    """
    A basic HTTP response with content, headers, and out-bound cookies
    
    The class variable ``defaults`` specifies default values for
    ``content_type``, ``charset`` and ``errors``. These can be overridden
    for the current request via the registry.
    
    """
    
    # See http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
    HTTP_MAPPINGS = {
        100: 'CONTINUE',
        101: 'SWITCHING PROTOCOLS',
        200: 'OK',
        201: 'CREATED',
        202: 'ACCEPTED',
        203: 'NON-AUTHORITATIVE INFORMATION',
        204: 'NO CONTENT',
        205: 'RESET CONTENT',
        206: 'PARTIAL CONTENT',
        226: 'IM USED',
        300: 'MULTIPLE CHOICES',
        301: 'MOVED PERMANENTLY',
        302: 'FOUND',
        303: 'SEE OTHER',
        304: 'NOT MODIFIED',
        305: 'USE PROXY',
        306: 'RESERVED',
        307: 'TEMPORARY REDIRECT',
        400: 'BAD REQUEST',
        401: 'UNAUTHORIZED',
        402: 'PAYMENT REQUIRED',
        403: 'FORBIDDEN',
        404: 'NOT FOUND',
        405: 'METHOD NOT ALLOWED',
        406: 'NOT ACCEPTABLE',
        407: 'PROXY AUTHENTICATION REQUIRED',
        408: 'REQUEST TIMEOUT',
        409: 'CONFLICT',
        410: 'GONE',
        411: 'LENGTH REQUIRED',
        412: 'PRECONDITION FAILED',
        413: 'REQUEST ENTITY TOO LARGE',
        414: 'REQUEST-URI TOO LONG',
        415: 'UNSUPPORTED MEDIA TYPE',
        416: 'REQUESTED RANGE NOT SATISFIABLE',
        417: 'EXPECTATION FAILED',
        500: 'INTERNAL SERVER ERROR',
        501: 'NOT IMPLEMENTED',
        502: 'BAD GATEWAY',
        503: 'SERVICE UNAVAILABLE',
        504: 'GATEWAY TIMEOUT',
        505: 'HTTP VERSION NOT SUPPORTED'
    }
    
    def __init__(self, content='', headers={}, status_code=200):
        "Initialise our response, assuming everything is fine"
        
        self.status_code = status_code
        self.set_content(content)
        self._headers = headers
        self._headers['content-length'] = str(len(content))
        self.cookies = SimpleCookie()
        
        # lets assume text/html unless told otherwise
        if not 'content-type' in self.headers:
            self._headers['content-type'] = 'text/html'
        
    def get_status(self):
        "Get the status code and message, but make sure it's valid first"
        if self.status_code not in self.HTTP_MAPPINGS:
            # invalid code, so something has gone wrong
            self.status_code = 500
        return "%s %s" % (self.status_code, self.HTTP_MAPPINGS[self.status_code])
        
    def set_status(self, code):
        "API setter method"
        if self.status_code not in self.HTTP_MAPPINGS:
            # invalid code, so something has gone wrong
            self.status_code = 500
        else:
            self.status_code = code
        
    def get_headers(self):
        "Return the headers as a list"
        return list(self._headers.iteritems())
        
    def set_headers(self, *args):
        "Set the response headers, takes either a key/value or a dictionary"
        if type(args[0]).__name__ == 'dict':
            self._headers.update(args[0])
        else:
            key, value = args
            self._headers[key] = value
        
    def get_content(self):
        "Return the body of the response in a useful format"
        return [self._content, '\n']
        
    def set_content(self, value):
        "Set the body of the response, ensuring we're using utf-8"
        # http://www.python.org/dev/peps/pep-0333/#unicode-issues
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        self._content = value
    
    def set_cookie(self, key, value='', max_age=None, expires=None, path='/',
                   domain=None, secure=None, httponly=None):
        """
        Define a cookie to be sent via the outgoing HTTP headers
        """
        self.cookies[key] = value
        for var_name, var_value in [
            ('max_age', max_age), ('path', path), ('domain', domain),
            ('secure', secure), ('expires', expires), ('httponly', httponly)]:
            if var_value is not None and var_value is not False:
                self.cookies[key][var_name.replace('_', '-')] = var_value
    
    def delete_cookie(self, key, path='/', domain=None):
        """
        Notify the browser the specified cookie has expired and should be
        deleted (via the outgoing HTTP headers)
        """
        self.cookies[key] = ''
        if path is not None:
            self.cookies[key]['path'] = path
        if domain is not None:
            self.cookies[key]['domain'] = domain
        self.cookies[key]['expires'] = 0
        self.cookies[key]['max-age'] = 0
        
    content = property(get_content, set_content)
    status = property(get_status, set_status)
    headers = property(get_headers, set_headers)
    
    def __str__(self):
        """Returns a rendition of the full HTTP message, including headers.
        
        When the content is an iterator, the actual content is replaced with the
        output of str(iterator) (to avoid exhausting the iterator).
        """
        if self._is_str_iter:
            content = ''.join(self.get_content())
        else:
            content = str(self.content)
        return '\n'.join(['%s: %s' % (key, value)
            for key, value in self.headers.headeritems()]) \
            + '\n\n' + content
    
    def __call__(self, environ, start_response):
        """
        Convenience call to return output and set status information
        
        Conforms to the WSGI interface for calling purposes only.
        
        Example usage:
        
        .. code-block:: python
        
            def wsgi_app(environ, start_response):
                response = WSGIResponse()
                response.write("Hello world")
                response.headers['Content-Type'] = 'latin1'
                return response(environ, start_response)
        
        """
        for c in self.cookies.values():
            self.headers.append(('Set-Cookie', c.output(header='')))
        start_response(self.status, self.headers)
        is_file = isinstance(self.content, file)
        if 'wsgi.file_wrapper' in environ and is_file:
            return environ['wsgi.file_wrapper'](self.content)
        elif is_file:
            return iter(lambda: self.content.read(), '')
        return self.get_content()


class WSGIResponseRedirect(WSGIResponse):
    "Sub class of HttpResponse making redirects easier to handle"
    def __init__(self, redirect_location, permanent=True):
        super(WSGIResponseRedirect, self).__init__()
        self._headers['Location'] = redirect_location
        # allow us to set whether we want a 301 or 302 redirect
        if permanent:
            self.status_code = 301
        else:
            self.status_code = 302


class WSGINotFound(WSGIResponse):
    "Sub class of HttpResponse making 404's easier to handle"
    def __init__(self):
        super(WSGINotFound, self).__init__()
        self.status_code = 404

class WSGIMethodNotAllowed(WSGIResponse):
    "Sub class of HttpResponse making 500's easier to handle"
    def __init__(self):
        super(WSGIMethodNotAllowed, self).__init__()
        self.status_code = 405