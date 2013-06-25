import re
import sys
import subprocess
import json

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
	return '<?xml version="1.0"?>\n<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n\t'

def execPHPScript(url, getfield):
    cmd = 'php index.php %s %s' % (url, getfield)
    # execute a php script which retrieves the json-object from twitter
    # and stores it into a .json-file
    subprocess.call(cmd.split(), stdout=openWriteFile(inputFile))

def parse(inputFile, outputFile, userURL):
    f = openReadFile(inputFile)
    tmp = json.load(f)  # load data from file
    #data = json.dumps(tmp, sort_keys=True, indent=2) # use json.dumps because of possibility of using different options

    #output = initXML()
    outputRdf = initRDF()
    
    # root
    #output += '<tweet>\n\t'
    outputRdf += '<rdf:Description rdf:about="">\n\t\t<tweet>\n\t\t\t'

    # name
    #output += '<user>\n\t\t<name>' + tmp[0]['user']['name'] + '</name>\n\t\t'
    outputRdf += '<rdf:Description rdf:about="' + sys.argv[1] + '">\n\t\t\t\t<user>\n\t\t\t\t\t<rdf:Description rdf:about="' + userURL + '">\n\t\t\t\t\t\t<name>' + tmp[0]['user']['name'] + '</name>\n\t\t\t\t\t\t'
    
    # twitter-name
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
    #f.write(str(output))

    f2 = openWriteFile(outputFile2)
    f2.write(str(outputRdf))
    
def main(completeUrl):
    # split url with delimiter "?" and "&" in 5 elements (stored in a list)
    splittedUrl = re.split("([?, &])", completeUrl)
    url = splittedUrl[0]
    getfield = splittedUrl[1] + splittedUrl[2]
    userURL = splittedUrl[0] + splittedUrl[1] + splittedUrl[2]
    
    #command = "php index.php https://api.twitter.com/1.1/statuses/user_timeline.json ?screen_name=sbahnberlin&count=1"
    execPHPScript(url, getfield)
    # pass among other things userURL for .rdf-file
    parse(inputFile, outputFile, userURL)

if __name__ == "__main__":
    main()
    if len(sys.argv) != 2:
        print 'run as: python main.py <url>'
    else:
        main(sys.argv[1])