# -*- coding: utf-8 -*-
from common import *

class WSGIRequestTest(WsgiTestCase):

    def testValidRequestTypes(self):
        for request_method in ('POST', 'GET', 'DELETE', 'PUT', 'HEAD', 'OPTIONS', 'TRACE'):
            env = self.env.mock(method=request_method, query='')
            self.assertEquals(WSGIRequest(env).method, request_method)
    
    def testInvalidRequestTypes(self):
        for request_method in [ 'notPOST', 'GETnot', 'DELETE!', '±PUT', '?HEAD', '.OPTIONS', '\TRACE' ]:
            env = self.env.mock(method=request_method)
            self.assertRaises(WSGIError, WSGIRequest, env)
    
    def testSimpleQueryString(self):
        query_string = 'x=y&1=2'
        env = self.env.mock(method='GET', query=query_string)
        self.assertEquals(WSGIRequest(env).GET, {'1': '2', 'x': 'y'})
    
    def testNestedQueryString(self):
        query_string = 'x=y&x=z&1=2'
        env = self.env.mock(method='GET', query=query_string)
        self.assertEquals(WSGIRequest(env).GET, {'1': '2', 'x': ['y', 'z']})
    
    def testArrayNotationNestedQueryString(self):
        query_string = 'x[]=y&x[]=z&1=2'
        env = self.env.mock(method='GET', query=query_string)
        self.assertEquals(WSGIRequest(env).GET, {'1': '2', 'x[]': ['y', 'z']})
    
if __name__ == "__main__":
    unittest.main();