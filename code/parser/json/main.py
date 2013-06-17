import re
import sys
import subprocess
import json

# Terminal: python main.py https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=sbahnberlin\&count=1

inputFile = 'sbahnberlin.json'
outputFile = 'sbahnberlin.xml'

def openReadFile(file):
    f = open(file, 'r')
    return f

def openWriteFile(file):
    f = open(file, 'w')
    return f

def execPHPScript(url, getfield):
    cmd = 'php index.php %s %s' % (url, getfield)
    # execute a php script which retrieves the json-object from twitter
    # and stores it into a .json-file
    subprocess.call(cmd.split(), stdout=openWriteFile(inputFile))

def parse(inputFile, outputFile):
    f = openReadFile(inputFile)
    tmp = json.load(f)  # load data from file
    #data = json.dumps(tmp, sort_keys=True, indent=2) # use json.dumps because of possibility of using different options

    # header
    output = '<?xml version="1.1" encoding="UTF-8" standalone="yes"?>\n<tweet>\n\t'

    # name
    output += '<user>\n\t\t<name>' + tmp[0]['user']['name'] + '</name>\n\t\t'
    
    # twitter-name
    output += '<twitter_name>' + tmp[0]['user']['screen_name'] + '</twitter_name>\n\t\t'
    
    # followers
    output += '<followers_count>' + str(tmp[0]['user']['followers_count']) + '</followers_count>\n\t\t'
    
    # status
    output += '<statuses_count>' + str(tmp[0]['user']['statuses_count']) + '</statuses_count>\n\t' + '</user>\n\t'

    # retweets
    output += '<retweet_count>' + str(tmp[0]['retweet_count']) + '</retweet_count>\n\t'

    # recent tweet
    output += '<text>' + tmp[0]['text'] + '</text>\n\t'

    # date
    output += '<created_at>' + tmp[0]['created_at'] + '</created_at>\n'

    # tail
    output += '</tweet>'

    output = u''.join(output).encode('utf-8').strip()
    
    f = openWriteFile(outputFile)
    f.write(str(output))
    
def main():
    if len(sys.argv) != 2:
        print 'run as: python main.py <url>'
    else:
        completeUrl = sys.argv[1]
        # split url with delimiter "?" in 3 elements (stored in a list)
        splittedUrl = re.split("([?])", completeUrl)
        url = splittedUrl[0]
        getfield = splittedUrl[1] + splittedUrl[2]
        #command = "php index.php https://api.twitter.com/1.1/statuses/user_timeline.json ?screen_name=sbahnberlin&count=1"
        execPHPScript(url, getfield)
        parse(inputFile, outputFile)

main()