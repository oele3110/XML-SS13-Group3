__all__=["filter"]

from logging_wrapper import *
from parserx.microdata import main
from parserx.linkeddata import linkeddata
from parserx.xml import parser2
import rdf

def filter(request, data):
    try:
        if request.responseHeaders.hasHeader("content-type"):
            content_types = request.responseHeaders.getRawHeaders(
                "content-type")

            if request.host.host == "stackoverflow.com" and\
                    any([x.find("text/html") >= 0 for x in content_types]):
                info("Filter stack overflow text/html resource.")
                rdf_ = main.run(request.uri, data)
                rdf.importDatasets(rdf_)
                info("Parser result: %s" % x)
	    elif request.host.host == "dbpedia.org":
		info("DBPEDIA URI: "+request.uri)
		rdf_ = linkeddata.run(request.uri)
		rdf.importDatasets(rdf_)
	    elif request.host.host.find("entscholar.net") >= 0:
		info("Entscholar URI: "+request.uri)
		rdf_ = parser2.parse_string(request.uri, data)
		rdf.importDatasets(rdf_)
	    else:
                info("Unknown content type, skip filtering")
        else:
            info("No content type specified, skip filtering")
    except Exception as e:
        error(e)
        raise
    return data
