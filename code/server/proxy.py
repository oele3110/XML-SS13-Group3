#!/usr/bin/python
"""A basic transparent HTTP proxy"""

__author__ = "Erik Johansson"
__email__  = "erik@ejohansson.se"
__license__= """
Copyright (c) 2012 Erik Johansson <erik@ejohansson.se>
 
This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
USA

"""

from twisted.web import http
from twisted.internet import reactor, protocol
from twisted.python import log
import re
import sys
import rdf

#modified begin
#disable logging
#log.startLogging(sys.stdout)
#modified end

class ProxyClient(http.HTTPClient):
    """ The proxy client connects to the real server, fetches the resource and
    sends it back to the original client, possibly in a slightly different
    form.
    """

    def __init__(self, method, uri, postData, headers, originalRequest):
        self.method = method
        self.uri = uri
        self.postData = postData
        self.headers = headers
        self.originalRequest = originalRequest
        self.contentLength = None

    def sendRequest(self):
        log.msg("Sending request: %s %s" % (self.method, self.uri))
        self.sendCommand(self.method, self.uri)

    def sendHeaders(self):
        for key, values in self.headers:
            if key.lower() == 'connection':
                values = ['close']
            elif key.lower() == 'keep-alive':
                next

            for value in values:
                self.sendHeader(key, value)
        self.endHeaders()

    def sendPostData(self):
        log.msg("Sending POST data")
        self.transport.write(self.postData)

    def connectionMade(self):
        log.msg("HTTP connection made")
        self.sendRequest()
        self.sendHeaders()
        if self.method == 'POST':
            self.sendPostData()

    def handleStatus(self, version, code, message):
        log.msg("Got server response: %s %s %s" % (version, code, message))
        self.originalRequest.setResponseCode(int(code), message)

    def handleHeader(self, key, value):
        if key.lower() == 'content-length':
            self.contentLength = value
        else:
            self.originalRequest.responseHeaders.addRawHeader(key, value)

    def handleResponse(self, data):
        if self.originalRequest.host.host == "api.twitter.com" and \
                self.originalRequest.uri.find("screen_name=") > 0:
            from parserx.json import main
            data, rdf_ = main.main(self.uri)
            rdf.importDatasets(rdf_)

            uri_ = str(self.originalRequest.uri)
            index1 = uri_.find("screen_name=")+len("screen_name=")
            index2 = uri_.find("&", index1)
            url_ = "https://twitter.com/%s" % uri_[index1:index2]

            from logging_wrapper import info
            import urllib2

            info("Fetch twitter url: %s" % url_)
            response = urllib2.urlopen(url_)
            page = response.read()

            info("Got twitter response")

            if page:
                data = page
                self.originalRequest.responseHeaders.setRawHeaders(
                    "content-type", ["text/html"])
                self.originalRequest.responseHeaders.setRawHeaders(
                    "content-encoding", [])
            else:
                #self.originalRequest.responseHeaders.setRawHeaders(
                #    "content-type", ["application/json"])
                self.originalRequest.responseHeaders.setRawHeaders(
                    "content-encoding", [])

        data = self.originalRequest.processResponse(data)
        if self.contentLength != None:
            self.originalRequest.setHeader('Content-Length', len(data))

        self.originalRequest.write(data)

        self.originalRequest.finish()
        self.transport.loseConnection()

class ProxyClientFactory(protocol.ClientFactory):
    def __init__(self, method, uri, postData, headers, originalRequest):
        self.protocol = ProxyClient
        self.method = method
        self.uri = uri
        self.postData = postData
        self.headers = headers
        self.originalRequest = originalRequest

    def buildProtocol(self, addr):
        return self.protocol(self.method, self.uri, self.postData,
                             self.headers, self.originalRequest)

    def clientConnectionFailed(self, connector, reason):
        log.err("Server connection failed: %s" % reason)
        self.originalRequest.setResponseCode(504)
        self.originalRequest.finish()

class ProxyRequest(http.Request):
    def __init__(self, channel, queued, reactor=reactor):
        http.Request.__init__(self, channel, queued)
        self.reactor = reactor

    def process(self):
        host = self.getHeader('host')
        if not host:
            log.err("No host header given")
            self.setResponseCode(400)
            self.finish()
            return

        port = 80
        if ':' in host:
            host, port = host.split(':')
            port = int(port)

        self.setHost(host, port)

        self.content.seek(0, 0)
        postData = self.content.read()
        factory = ProxyClientFactory(self.method, self.uri, postData,
                                     self.requestHeaders.getAllRawHeaders(),
                                     self)
        self.reactor.connectTCP(host, port, factory)

    def processResponse(self, data):
        #modified begin
        import proxy_filter
        from logging_wrapper import info

        content_encoding = self.responseHeaders.getRawHeaders(
            "content-encoding")
        content_types = self.responseHeaders.getRawHeaders(
            "content-type")
        info("Got: %s, %s" % (self.host.host, self.uri))
        #print content_encoding, content_types
        gzipped = data and content_encoding\
            and any([x.find("gzip") >= 0 for x in content_encoding])\
            and content_types and (
            any([x.find("text/html") >= 0 for x in content_types]) or 
            any([x.find("text/xml") >= 0 for x in content_types])
            )

        if gzipped:
            import gzip
            from StringIO import StringIO
            info("Decompress response")
            buf = StringIO(data)
            s = gzip.GzipFile(mode="rb", fileobj=buf)
            data = s.read()

        data = proxy_filter.filter(self, data)
        if gzipped:
            #self.responseHeaders.removeHeader("content-encoding")
            import gzip
            from StringIO import StringIO
            buf = StringIO()
            s = gzip.GzipFile(mode="wb", fileobj=buf, compresslevel=2)
            s.write(data)
            s.close()
            data = buf.getvalue()

        # #modified end
        return data

class TransparentProxy(http.HTTPChannel):
    requestFactory = ProxyRequest
 
class ProxyFactory(http.HTTPFactory):
    protocol = TransparentProxy
 
#modfied begin
#reactor.listenTCP(8080, ProxyFactory())
#reactor.run()

def get_proxy_server(port):
    import threading
    #log.startLogging(open(".log", "w"))#stop logging
    reactor.listenTCP(port, ProxyFactory())
    return threading.Thread(target=reactor.run)
#modified end
