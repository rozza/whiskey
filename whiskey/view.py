from exceptions import WSGIError

class BaseView(object):
    
    def __init__(self, app, request):
        self.app = app
        self.request = request
    
    def GET(self):
        raise WSGIError()
    POST = DELETE = PUT = GET

    def HEAD(self):
        return self.GET()