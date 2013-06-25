import re
import sys
import subprocess
import json
import datetime

# Terminal: python main.py https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=sbahnberlin\&count=1

inputFile = 'sbahnberlin.json'
outputFile = 'sbahnberlin.xml'
outputFile2 = 'sbahnberlin.rdf'

def openReadFile(file):
    f = open(file, 'r')
    return f

def openWriteFile(file):
    f = open(file, 'w')
    return f

"""def initXML():
	return '<?xml version="1.1" encoding="UTF-8" standalone="yes"?>\n'"""

def initRDF():
	return '<?xml version="1.0"?>\n<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n\txmlns:sioc="http://rdfs.org/sioc/ns#"\n\txmlns:dcterms="http://purl.org/dc/terms#"\n\txmlns:xsd="http://www.w3.org/2001/XMLSchema#">\n\t'

def getTimestamp():
	return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S');

def execPHPScript(url, getfield):
    if __name__ == "__main__":
        cmd = 'php index.php %s %s' % (url, getfield)
    else:
        cmd = 'php server/parserx/json/index.php %s %s' % (url, getfield)
    # execute a php script which retrieves the json-object from twitter
    # and stores it into a .json-file
    subprocess.call(cmd.split(), stdout=openWriteFile(inputFile))

def parse(inputFile, outputFile, completeURL, userURL, splittedUrl):
    f = openReadFile(inputFile)
    tmp = json.load(f)  # load data from file
    #data = json.dumps(tmp, sort_keys=True, indent=2) # use json.dumps because of possibility of using different options

    #output = initXML()
    outputRdf = initRDF()
    
    # root - tweet
    #output += '<tweet>\n\t'
    outputRdf += '<rdf:Description rdf:about="' + userURL + '&amp;' + splittedUrl[4] + '">\n\t\t'
    
    # xsd:dateTime
    outputRdf += '<xsd:dateTime>' + getTimestamp() + '</xsd:dateTime>\n\t\t'

    # dcterms:publisher
    #output += '<user>\n\t\t<name>' + tmp[0]['user']['name'] + '</name>\n\t\t'
    outputRdf += '<dcterms:publisher rdf:resource="' + userURL + '"/>\n\t\t'
    
    # sioc:content
    outputRdf += '<sioc:content>' + tmp[0]['text'] + '</sioc:content>\n\t\t'
    
    # sioc:num_replies
    outputRdf += '<sioc:num_replies>' + str(tmp[0]['retweet_count']) + '</sioc:num_replies>\n\t\t'
    
    # dcterms:created_at
    outputRdf += '<dcterms:created_at>' + tmp[0]['created_at'] + '</dcterms:created_at>\n\t</rdf:Description>\n\t'
    
    # root - twitter user
    outputRdf += '<rdf:Description rdf:about="' + userURL + '">\n\t\t'
    
    # sioc:name
    outputRdf += '<sioc:name>' + tmp[0]['user']['screen_name'] + '</sioc:name>\n\t\t'
    
    # sioc:account_of
    outputRdf += '<sioc:account_of>' + tmp[0]['user']['name'] + '</sioc:account_of>\n\t\t'
    
    # TODO - followers
    #outputRdf += '<>' + str(tmp[0]['user']['followers_count']) + '</>'
    
    # sioc:num_items
    outputRdf += '<sioc:num_items>' + str(tmp[0]['user']['statuses_count']) + '</sioc:num_items>\n\t'
    
    # tail
    outputRdf += '</rdf:Description>\n</rdf:RDF>'
    
    outputRdf = u''.join(outputRdf).encode('utf-8').strip()
    
    
    """# twitter-name
    #output += '<twitter_name>' + tmp[0]['user']['screen_name'] + '</twitter_name>\n\t\t'
    outputRdf += '<twitter_name>' + tmp[0]['user']['screen_name'] + '</twitter_name>\n\t\t\t\t\t\t'
    
    # followers
    #output += '<followers_count>' + str(tmp[0]['user']['followers_count']) + '</followers_count>\n\t\t'
    outputRdf += '<followers_count>' + str(tmp[0]['user']['followers_count']) + '</followers_count>\n\t\t\t\t\t\t'
    
    # status
    #output += '<statuses_count>' + str(tmp[0]['user']['statuses_count']) + '</statuses_count>\n\t' + '</user>\n\t'
    outputRdf += '<statuses_count>' + str(tmp[0]['user']['statuses_count']) + '</statuses_count>\n\t\t\t\t\t</rdf:Description>\n\t\t\t\t' + '</user>\n\t\t\t\t'

    # retweets
    #output += '<retweet_count>' + str(tmp[0]['retweet_count']) + '</retweet_count>\n\t'
    outputRdf += '<retweet_count>' + str(tmp[0]['retweet_count']) + '</retweet_count>\n\t\t\t\t'

    # recent tweet
    #output += '<text>' + tmp[0]['text'] + '</text>\n\t'
    outputRdf += '<text>' + tmp[0]['text'] + '</text>\n\t\t\t\t'

    # date
    #output += '<created_at>' + tmp[0]['created_at'] + '</created_at>\n'
    outputRdf += '<created_at>' + tmp[0]['created_at'] + '</created_at>\n\t\t\t</rdf:Description>\n\t\t'

    # tail
    #output += '</tweet>'
    outputRdf += '</tweet>\n\t</rdf:Description>\n</rdf:RDF>'

    #output = u''.join(output).encode('utf-8').strip()
    outputRdf = u''.join(outputRdf).encode('utf-8').strip()
    
    #f = openWriteFile(outputFile)
    #f.write(str(output))"""

    if __name__ == "__main__":
        f2 = openWriteFile(outputFile2)
        f2.write(str(outputRdf))
    else:
        return "".join([l for l in open(inputFile)]), str(outputRdf)
    
def main(completeUrl):
    # split url with delimiter "?" and "&" in 5 elements (stored in a list)
    splittedUrl = re.split("([?, &])", completeUrl)
    url = splittedUrl[0]
    getfield = splittedUrl[1] + splittedUrl[2]
    userURL = splittedUrl[0] + splittedUrl[1] + splittedUrl[2]
    
    #command = "php index.php https://api.twitter.com/1.1/statuses/user_timeline.json ?screen_name=sbahnberlin&count=1"
    execPHPScript(url, getfield)
    # pass among other things userURL for .rdf-file
    return parse(inputFile, outputFile, completeUrl, userURL, splittedUrl)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print 'run as: python main.py <url>'
    else:
        main(sys.argv[1])
