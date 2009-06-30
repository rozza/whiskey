import re
from request import WSGIRequest
from exceptions import WSGIError
from response import WSGINotFound, WSGIMethodNotAllowed

class WebAppInterface(object):
    """
    The Web Application Interface
    """
    def __init__(self, routes, views):
        self.routes = routes
        self.views = views
        
    def __call__(self, environ, start_response):
        response = WSGINotFound()
        return response(environ, start_response)
    
class WebApp(WebAppInterface):
    """
    An interface to a web.py like application.  It works like the web.run
    function in web.py
    
   routes = (
        (r'^/foo/([0-9]+)/([0-9]+)', 'Foo'),
        (r'^/bar$', 'Bar'),
        ('/.*', 'NotFoundPageHandler'),
    )
    
    """
    
    def __init__(self, routes, views):
        self.routes = [(re.compile('^%s$' % routes[i]), routes[i + 1])
                     for i in xrange(0, len(routes), 2)]
        self.views = views
        
    def __call__(self, environ, start_response):
        try:
            request = WSGIRequest(environ)
            for regex, view in self.routes:
                match = regex.match(environ['PATH_INFO'])
                if match is not None:
                    if not callable(view):
                        view = self.views[view]
                    view = view(self, request)
                    response = getattr(view, request.method)(*match.groups(), **match.groupdict())
                    break
            else:
                response = WSGINotFound()
        except WSGIError, e:
            response = WSGIMethodNotAllowed()
        return response(environ, start_response)


class TokenBasedApp(WebApp):
    """
    Example Application using a simple token based scheme for routing.
    This has the advantage of making reversing relatively simple. 
    Routes look like:
    
    routes = (
        ('/', Foo),
        ('/myview/:stuff/', Bar)
    )
    """
    
    def __init__(self, routes, views=None):
        self.routes = [(re.compile('^%s$' % self._route_master(route[0])), route[1]) for route in routes]
        self.views = views
    
    def _route_master(self, route):
        "returns a compiled regular expression"
        # chop off leading slash
        if route.startswith('/'):
            route = route[1:]
        
        trailing_slash = False
        # check end slash and remember to keep it
        if route.endswith('/'):
            route = route[:-1]
            trailing_slash = True
        
        # split into path components
        bits = route.split('/')
        
        # compiled match starts with a slash,
        #  so we make it a list so we can join later
        regex = ['']
        for path_component in bits:
            if path_component.startswith(':'):
                # it's a route, so compile
                name = path_component[1:]
                # accept only valid URL characters
                regex.append(r'(?P<%s>[-_a-zA-Z0-9+%%]+)' % name)
            else:
                # just a string/static path component
                regex.append(path_component)
            
        # stick the trailing slash back on
        if trailing_slash:
            regex.append('')
        
        # stitch it back together as a path
        return '^%s$' % '/'.join(regex)      