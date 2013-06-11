__all__ = ["ResourceServerHandler"]

from BaseHTTPServer import BaseHTTPRequestHandler

class ResourceServerHandler(BaseHTTPRequestHandler):

    def create_header(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        pass

    def create_body(self):
        self.wfile.write(str(dir(self)))
        pass

    def respond(self):
        self.create_header()
        self.create_body()
        pass

    def do_GET(self):
        return self.respond()

    def do_POST(self):
        return self.respond()

    pass
