from whiskey import *

routes = (
    ('/', 'index'),
    ('/about', 'about'),
)

class BaseView(object):
    
    def __init__(self, application, request):
        self.application = application
        self.request = request
    
    def GET(self):
        raise WSGIError()
    POST = DELETE = PUT = GET

    def HEAD(self):
        return self.GET()


class index(BaseView):
    
    def GET(self):
        return WSGIResponse('Hello World')


class about(BaseView):
    
    def GET(self):
        return WSGIResponse('This is the about page')

application = WebApp(routes, globals())

if __name__ == '__main__':
    run(application)