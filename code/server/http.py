__all__ = ["get_http_server"]

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse as parse_path
from urllib2 import urlparse
from history import getHistory

from logging_wrapper import *

class ResourceServerHandler(BaseHTTPRequestHandler):

    def prepare(self):
        self.url = parse_path(self.path)
        self.url_params = urlparse.parse_qs(self.url.query)
        pass

    def create_header(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        pass        

    def create_body(self):
        #debug(self.url)
        #debug(self.url_params)
	html = getHistory()
	self.wfile.write(html)
	
        #self.wfile.write((self.url, self.url_params))	
        pass

    def respond(self):
        self.prepare()
        self.create_header()
        self.create_body()
        pass

    def do_GET(self):
        return self.respond()

    def do_POST(self):
        return self.respond()
    pass

def get_http_server(port):
    import threading
    server = HTTPServer(('', port),
                        ResourceServerHandler)

    return threading.Thread(target=server.serve_forever,
                            args=())
