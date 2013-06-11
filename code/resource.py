__all__ = ["ResourceServerHandler"]

from BaseHTTPServer import BaseHTTPRequestHandler
from urlparse import urlparse as parse_path
from urllib2 import urlparse

from retrieve import handle_retrieve_request
from history import handle_history_request
from logging import *
from html_templates import OUTPUT_TEMPLATE

HANDLERS = {
    "retrieve": handle_retrieve_request,
    "history": handle_history_request
    }

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
    
    def parse_links(self, html_str):
        html_str = html_str.replace("RET_URL:", "/?action='retrieve'&params='")
        html_str = html_str.replace("HIS_URL:", "/?action='history'&params='")
        return html_str
        

    def create_body(self):
        #debug(self.url)
        #debug(self.url_params)

        ret = "No handler found."
        if "action" in self.url_params:
            params = None
            if not "params" in self.url_params:
                params = self.url_params
            action = HANDLERS[self.url_params["action"][0]]
            ret = action(self.url, params)

        ret = self.parse_links(ret)

        self.wfile.write(OUTPUT_TEMPLATE % ret)
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
