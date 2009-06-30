# -*- coding: utf-8 -*-
from common import *

class TestRouting(WsgiTestCase):
    def testBasicRouting(self):
        class slash(BaseView):
            def GET(self):
                return WSGIResponse('success')
        
        routes = (('/', 'slash'),)
        
        self.mock_token_request(routes=routes, path='/', views=locals())
        
    def testBasicRoutingWithNamedArgs(self):
        class stuff(BaseView):
            
            def GET(self, *args, **kwargs):
                response = WSGIResponse()
                response.content = str(kwargs)
                return response
        
        routes = (
            ('/:stuff', 'stuff'),
            ('/:my/:things', 'stuff')
        )
        
        self.mock_token_request(routes=routes, path='/routingstuff', views=locals())
        self.assertContentEquals("{'stuff': 'routingstuff'}")
        
        self.mock_token_request(routes=routes, path='/meine/Dingen', views=locals())
        self.assertContentEquals("{'things': 'Dingen', 'my': 'meine'}")
    
    def testRoutingFailure(self):
        routes    = ()
        self.mock_token_request(routes=routes, path='/routingstuff')
        self.assertStatusEquals('404 NOT FOUND')
    
    def testMethodBasedRouting(self):
        class route(BaseView):
            def POST(self):
                return WSGIResponse('route.POST')
            def GET(self):
                return WSGIResponse('route.GET')
            def DELETE(self):
                return WSGIResponse('route.DELETE')
            def PUT(self):
                return WSGIResponse('route.PUT')
            def HEAD(self):
                return WSGIResponse('route.HEAD')
            def OPTIONS(self):
                return WSGIResponse('route.OPTIONS')
            def TRACE(self):
                return WSGIResponse('route.TRACE')
                
        routes    = (('/', 'route'),)
        for method in ('POST', 'GET', 'DELETE', 'PUT', 'HEAD', 'OPTIONS', 'TRACE'):
            self.mock_token_request(routes=routes, path='/', method=method, views=locals())
            self.assertContentEquals('route.%s' % method)
        
    def testMethodBasedRoutingFailure(self):
        class route(BaseView):
            def GET(self):
                return WSGIResponse('route.GET')

        routes = (('/', 'route'),)
        self.mock_token_request(routes=routes, path='/', method='POST', views=locals())
        self.assertStatusEquals('405 METHOD NOT ALLOWED')
        
    def testDefaultHeadRouting(self):
        """HEAD requests should be routed to GET if HEAD method doesn't exist"""
        class route(BaseView):
            def GET(self):
                return WSGIResponse('route.GET')
                
        routes    = (('/', 'route'),)
        self.mock_token_request(routes=routes, path='/', method="HEAD", views=locals())
        self.assertContentEquals('route.GET')

class TestRouteMaster(WsgiTestCase):
    
    def setUp(self):
        routes = (('/', 'stubb'),)
        self.token_app = TokenBasedApp(routes)
    
    def testBasicRegexGeneration(self):
        """TokenBasedApp._route_master should generate a regex from a string"""
        self.assertEquals(self.token_app._route_master('/'), r'^/$')
    
    def testInitialSlash(self):
        """A leading `/` will be prepended if it doesn't exist"""
        self.assertEquals(self.token_app._route_master('/foo'), r'^/foo$')
        self.assertEquals(self.token_app._route_master('foo'), r'^/foo$')
    
    def testTrailingSlash(self):
        """Trailing slashes will be retained in the regex"""
        self.assertEquals(self.token_app._route_master('/foo/'), r'^/foo/$')
    
    def testComponent(self):
        """Named components in the route generate named bits of regex"""
        self.assertEquals(self.token_app._route_master('/:foo'), r'^/(?P<foo>[-_a-zA-Z0-9+%]+)$')
        self.assertEquals(self.token_app._route_master('/:foo:foo'), r'^/(?P<foo:foo>[-_a-zA-Z0-9+%]+)$')
        self.assertEquals(self.token_app._route_master('/:123'), r'^/(?P<123>[-_a-zA-Z0-9+%]+)$')
        self.assertEquals(self.token_app._route_master('/:fo/o:foo'), r'^/(?P<fo>[-_a-zA-Z0-9+%]+)/o:foo$')
        self.assertEquals(self.token_app._route_master('/::fo/o:foo'), r'^/(?P<:fo>[-_a-zA-Z0-9+%]+)/o:foo$')


if __name__ == '__main__':
    unittest.main()