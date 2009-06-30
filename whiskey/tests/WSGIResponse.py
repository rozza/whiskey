# -*- coding: utf-8 -*-
from common import *

class WSGIResponseTest(WsgiTestCase):
    
  def testDefaultStatus(self):
    """WSGIResponse should have a status of 200 when none is specified"""
    result = WSGIResponse()
    self.assertEqual(result.status, '200 OK')
  
  def testDefaultHeaders(self):
    """WSGIResponse should create default content-length/type headers"""
    result = WSGIResponse('content')
    self.assertEqual(result.status,  '200 OK')
    self.assertEqual(result.headers, [
      ('content-length',  '7'),
      ('content-type',    'text/html')
    ])
  
  def testDefaultEndOfContent(self):
    """WSGIResponse should append a newline character to content."""
    result = WSGIResponse('content')
    self.assertEqual(result.status,  '200 OK')
    self.assertEqual(result.content, [
      'content',
      '\n'
    ])
  
  def testHeaderAddition(self):
    """I don't really think that Brad's `set_header` makes sense, but this is what it does"""
    result = WSGIResponse('content')
    result.headers = { 'x-test-header': 'a test!' }
    self.assertEqual(result.headers, [
      ('x-test-header',   'a test!'),
      ('content-length',  '7'),
      ('content-type',    'text/html')
    ])
    
    result.set_headers('x-test-header2', 'another test!')
    self.assertEqual(result.headers, [
      ('x-test-header',   'a test!'),
      ('content-length',  '7'),
      ('content-type',    'text/html'),
      ('x-test-header2',  'another test!')
    ])


if __name__ == "__main__":
  unittest.main();