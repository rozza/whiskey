import sys

# Server Adapters
def wsgiref_adapter(host, port, application):
    from wsgiref.simple_server import make_server
    srv = make_server(host, port, application)
    srv.serve_forever()

def appengine_adapter(host, port, application):
    from google.appengine.ext.webapp import util
    util.run_wsgi_app(application)

def cherrypy_adapter(host, port, application):
    # Experimental (Untested).
    from cherrypy import wsgiserver
    server = wsgiserver.CherryPyWSGIServer((host, port, application), application)
    server.start()

def flup_adapter(host, port, application):
    # Experimental (Untested).
    from flup.server.fcgi import WSGIServer
    WSGIServer(application, bindAddress=(host, port, application)).run()

def paste_adapter(host, port, application):
    # Experimental (Untested).
    from paste import httpserver
    httpserver.serve(application, host=host, port=str(port))

def django_adapter(host, port, application):
    from django.core.server.basehttp import run
    run(host, port, application)

def twisted_adapter(host, port, application):
    from twisted.application import service, strports
    from twisted.web import server, http, wsgi
    from twisted.python.threadpool import ThreadPool
    from twisted.internet import reactor
    
    thread_pool = ThreadPool()
    thread_pool.start()
    reactor.addSystemEventTrigger('after', 'shutdown', thread_pool.stop)
    
    resource = wsgi.WSGIResource(reactor, thread_pool, application)
    site = server.Site(resource)
    reactor.listenTCP(port, site)
    reactor.run()

WSGI_ADAPTERS = {
    'wsgiref': wsgiref_adapter,
    'appengine': appengine_adapter,
    'cherrypy': cherrypy_adapter,
    'django': django_adapter,
    'flup': flup_adapter,
    'paste': paste_adapter,
    'twisted': twisted_adapter,
}

# Server
def run(application, server='wsgiref', host='localhost', port=8080, config=None):
    """
    Runs the whiskey web server.
    
    Accepts an optional host (string), port (integer), server (string) and
    config (python module name/path as a string) parameters.
    
    By default, uses Python's built-in wsgiref implementation. Specify a server
    name from WSGI_ADAPTERS to use an alternate WSGI server.
    """
    if not server in WSGI_ADAPTERS:
        raise RuntimeError("Server '%s' is not a valid server. Please choose a different server.")
    
    if config is not None:
        # We'll let ImportErrors bubble up.
        config_options = __import__(config)
        host = getattr(config_options, 'host', host)
        port = getattr(config_options, 'port', port)
        server = getattr(config_options, 'server', server)
    
    # AppEngine seems to echo everything, even though it shouldn't. Accomodate.
    if server != 'appengine':
        print 'Whiskey starting up (using %s)...' % server
        print 'Listening on http://%s:%s...' % (host, port)
        print 'Use Ctrl-C to quit.'
        print
    
    try:
        WSGI_ADAPTERS[server](host, port, application)
    except KeyboardInterrupt:
        if server != 'appengine':
            print "Shuting down..."
        
        sys.exit()