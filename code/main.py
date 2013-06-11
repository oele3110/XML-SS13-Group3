from logging_wrapper import *
from resource import ResourceServerHandler
from BaseHTTPServer import HTTPServer

def launch_server():
    try:
        server = HTTPServer(('', 8345),
                            ResourceServerHandler)
        info("Started HTTP-Server")
        server.serve_forever()
    except KeyboardInterrupt:
        info("Ctrl-C received, shut down")
        server.socket.close()

if __name__ == "__main__":
    launch_server()
