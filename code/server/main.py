from http import get_http_server
from proxy import get_proxy_server
from logging_wrapper import *
import time
import rdf

HTTP_PORT = 8345
PROXY_PORT = 8346

def launch_servers():
    #rdf.disconnectDatabase()
    #if not rdf.connectDatabase():
    #    rdf.createDatabase()
    #    rdf.connectDatabase()

    rdf.disconnectDatabaseHttp()
    rdf.connectDatabaseHttp()

    http_server = get_http_server(HTTP_PORT)
    proxy_server = get_proxy_server(PROXY_PORT)
    
    http_server.daemon = True
    proxy_server.daemon = True

    try:
        info("Start HTTP-Server")
        http_server.start()
        info("Start Proxy-Server")
        proxy_server.run() #should be proxy_server.start()
        #while True:
        #    time.sleep(10)
    except KeyboardInterrupt:#caught in proxy_server...
        info("Quit!")
        rdf.disconnectDatabase()
    pass

if __name__ == "__main__":
    launch_servers()
