__all__=["filter"]

from logging_wrapper import *

def filter(request, data):
    try:
        if request.responseHeaders.hasHeader("content-type"):
            content_types = request.responseHeaders.getRawHeaders(
                "content-type")
            if any([x.find("text/html") >= 0 for x in content_types]):
                info("Filter text/html resource.")
            #elif any([...
            else:
                info("Unknown content type, skip filtering")
        else:
            info("No content type specified, skip filtering")
    except Exception as e:
        error(e)
        raise
    return data
