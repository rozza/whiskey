from whiskey import *


routes = (
    ('/', 'index'),
    ('/about', 'about'),
)


class index(BaseView):
    
    def GET(self):
        return WSGIResponse('Hello World')


class about(BaseView):
    
    def GET(self):
        return WSGIResponse('This is the about page')

app = WebApp(routes, globals())

if __name__ == '__main__':
    run(app)