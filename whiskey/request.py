import cgi
from exceptions import WSGIError

class WSGIRequest(object):
    """
    Our request object which stores information about the WSGI request
    """
    
    def __init__(self, environ):
        """
        Initialise our request with an environment
        """
        self.GET = self.POST = self.PUT = {}
        self.environ = environ
        
        # http://www.w3.org"/Protocols/rfc2616/rfc2616-sec9.html
        if self.method not in ("POST", "GET", "DELETE", "PUT", "HEAD", 
                                "OPTIONS", "TRACE"):
            raise WSGIError, "Invalid request"
        
        # if we have any query string arguments then we'll make then
        # more easily accessible
        if len(environ["QUERY_STRING"]):
            self.GET = self.clean_get()
        
        # Clean POST data
        if self.method == "POST":
            self.POST = self.clean_post()
        
        # Clean PUT data
        if self.method == "PUT":
            self.PUT = self.clean_post()
    
    @property
    def method(self):
        """
        Allow easy access to the request method
        """
        return self.environ["REQUEST_METHOD"]
    
    def clean_get(self):
        """
        Cleans the GET data
        
        Handles multiple key occurances in the GET data
        
        """
        raw_query_dict = cgi.parse_qs(self.environ["QUERY_STRING"], keep_blank_values=1)
        query_dict = {}
        
        for key, value in raw_query_dict.items():
            if len(value) <= 1:
                query_dict[key] = value[0]
            else:
                # Since it's a list of multiple items, we must have seen more than
                # one item of the same name come in. Store all of them.
                query_dict[key] = value
        
        return query_dict
    
    def clean_post(self):
        """
        Cleans the POST data
        
        Handles multiple key occurances in the POST data
        """
        raw_data = cgi.FieldStorage(fp=self.environ["wsgi.input"], 
                                         environ=self.environ,
                                         keep_blank_values=1)
        post_dict = {}
        
        for field in raw_data:
            if isinstance(raw_data[field], list):
                # Since it's a list of multiple items, we must have seen more than
                # one item of the same name come in. Store all of them.
                post_dict[field] = [fs.value for fs in raw_data[field]]
            elif raw_data[field].filename:
                # We've got a file.
                post_dict[field] = raw_data[field]
            else:
                post_dict[field] = raw_data[field].value
        
        return post_dict