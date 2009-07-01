import os, sys, re
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from whiskey import *

class BaseView(object):
    
    def __init__(self, application, request):
        self.application = application
        self.request = request
    
    def GET(self):
        raise WSGIError()
    POST = DELETE = PUT = GET
    
    def HEAD(self):
        return self.GET()

urls = (
    '/',        'index',
    '/about',   'about'
)

class index(BaseView):
    
    def GET(self):
        return WSGIResponse('Hello World')


class about(BaseView):
    
    def GET(self):
        return WSGIResponse('This is the about page')


class WebPyApp(WebApp):
    """
    An interface to a web.py like application.  It works like the web.run
    function in web.py
    """
    
    def __init__(self, routes, views):
        self.routes = [(re.compile('^%s$' % routes[i]), routes[i + 1])
                     for i in xrange(0, len(routes), 2)]
        self.views = views


application = WebPyApp(urls, globals())

if __name__ == '__main__':
    run(application)