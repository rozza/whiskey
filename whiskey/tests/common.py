# -*- coding: utf-8 -*-
import os, sys, tempfile, unittest
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from whiskey import *

class MockWsgiEnv(object):
    def __init__(self):
        self.__base = {
            # REQUIRED WSGI Env. Variables
            'REQUEST_METHOD':     '',
            'SCRIPT_NAME':            '',
            'PATH_INFO':                '/',
            'QUERY_STRING':         '',
            'CONTENT_LENGTH':     '',
            'CONTENT_TYPE':         'text/plain',
            'SERVER_NAME':            'localhost',
            'SERVER_PORT':            '8000',
            'SERVER_PROTOCOL':    'HTTP/1.1',
            
            'HTTP_ACCEPT':                    'application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
            'HTTP_ACCEPT_ENCODING': 'gzip, deflate',
            'HTTP_ACCEPT_LANGUAGE': 'en-us',
            'HTTP_CONNECTION':            'keep-alive',
            'HTTP_HOST':                        '127.0.0.1:8000',
            'HTTP_USER_AGENT':            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-us) AppleWebKit/530.4+ (KHTML, like Gecko) Version/4.0 Safari/528.16',
            
            'wsgi.errors':                    sys.stderr,
            'wsgi.file_wrapper':        None,
            'wsgi.input':                     None,
            'wsgi.multiprocess':        False,
            'wsgi.multithread':         True,
            'wsgi.run_once':                False,
            'wsgi.url_scheme':            'http',
            'wsgi.version':                 (1, 0)
        }
        
    def mock(self, method='GET', path=None, query=''):
        cur = self.__base.copy()
        cur[ 'REQUEST_METHOD' ] = method
        cur[ 'PATH_INFO' ]            = path
        cur[ 'CONTENT_TYPE']        = 'application/x-www-form-urlencoded'
        if cur[ 'REQUEST_METHOD' ] == 'POST' or cur[ 'REQUEST_METHOD' ] == 'PUT':
            tmp = tempfile.TemporaryFile()
            tmp.write(query)
            tmp.seek(0)
            cur[ 'wsgi.input' ]     = tmp
        else:
            cur[ 'QUERY_STRING' ] = query
        return cur
    

class WsgiTestCase(unittest.TestCase):

    def setUp(self):
        self.env = MockWsgiEnv()
        self.last_response = {}
        self.routed_to = None
        self.routing_args = None
        
    def mock_token_request(self, method='GET', path=None, query='', routes=None, views=None):
        app = TokenBasedApp(routes, views)
        self.last_response['content'] = app.__call__(self.env.mock(
                                                        path=path,
                                                        method=method,
                                                        query=query
                                                    ), self.gather_response)
    
    def mock_request(self, method='GET', path=None, query='', routes=None, views=None):
        app = WebApp(routes, views)
        self.last_response['content'] = app.__call__(self.env.mock(
                                                        path=path,
                                                        method=method,
                                                        query=query
                                                    ), self.gather_response)
    
    def gather_response(self, status, header):
        self.last_response = {
            'status': status,
            'header': header
        }
    
    def assertResponseEquals(self, status, header):
        self.assertEquals(self.last_response[ 'status' ], status)
        self.assertEquals(self.last_response[ 'header' ], header)
    
    def assertContentEquals(self, content):
        self.assertEquals(self.last_response[ 'content' ], [ content, '\n' ])
    
    def assertStatusEquals(self, status):
        self.assertEquals(self.last_response[ 'status' ], status)
    
    def assertRoutedTo(self, target):
        self.assertEquals(self.routed_to, target)
    
    def assertRoutingArgs(self, args):
        self.assertEquals(self.routing_args, args)