import os, sys, re
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from whiskey import *

REQUEST_MAPPINGS = {
    'GET': [],
    'POST': [],
    'PUT': [],
    'DELETE': [],
}

# Decorators for exposing urls
def get(url):
    """Registers a method as capable of processing GET requests."""
    def wrapped(method):
        def new(*args, **kwargs):
            return method(*args, **kwargs)
        # Register.
        re_url = re.compile("^%s$" % url)
        REQUEST_MAPPINGS['GET'].append((re_url, url, new))
        return new
    return wrapped

def post(url):
    """Registers a method as capable of processing POST requests."""
    def wrapped(method):
        def new(*args, **kwargs):
            return method(*args, **kwargs)
        # Register.
        re_url = re.compile("^%s$" % url)
        REQUEST_MAPPINGS['POST'].append((re_url, url, new))
        return new
    return wrapped

def put(url):
    """Registers a method as capable of processing PUT requests."""
    def wrapped(method):
        def new(*args, **kwargs):
            return method(*args, **kwargs)
        # Register.
        re_url = re.compile("^%s$" % url)
        REQUEST_MAPPINGS['PUT'].append((re_url, url, new))
        return new
    return wrapped

def delete(url):
    """Registers a method as capable of processing DELETE requests."""
    def wrapped(method):
        def new(*args, **kwargs):
            return method(*args, **kwargs)
        # Register.
        re_url = re.compile("^%s$" % url)
        REQUEST_MAPPINGS['DELETE'].append((re_url, url, new))
        return new
    return wrapped

# Application
class IttyStyleApp(object):
    """
    An interface to a Itty style application
    """
    def __call__(self, environ, start_response):
        try:
            request = WSGIRequest(environ)
            response = WSGINotFound()
            for url_set in REQUEST_MAPPINGS[request.method]:
                match = url_set[0].search(environ['PATH_INFO'])
                
                if match:
                    response = url_set[2](*match.groups(), **match.groupdict())
                    break
        except WSGIError, e:
            response = WSGIMethodNotAllowed()
        return response(environ, start_response)

# Controllers

@get('/get/(?P<name>\w+)')
def test_get(request, name='world'):
    return WSGIResponse('Hello %s!' % name)

@post('/post')
def test_post(request):
    return WSGIResponse("'foo' is: %s" % request.POST.get('foo', 'not specified'))

@put('/put')
def test_put(request):
    return WSGIResponse("'foo' is: %s" % request.PUT.get('foo', 'not specified'))

@delete('/delete')
def test_delete(request):
    return WSGIResponse('Method received was %s.' % request.method)

application = IttyStyleApp()

if __name__ == '__main__':
    run(application)