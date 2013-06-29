import rdf
import re

def buildHeader():
	return "<html>\n<head>\n\t<title>history</title>\n</head>\n<body>\n<h1>History</h1>\n\n"

def buildFooter():
	return "\n</body>\n</html>"

def getHistory():
	
	query = "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT * WHERE {?s xsd:dateTime ?o}"
	#pattern1 = '\s*<binding name="s"><uri>(.*)</uri></binding>\s*'
	#pattern2 = '\s*<binding name="o"><literal>(.*)</literal></binding>\s*'
	pattern = '|\s*<(.*)>\s*|\s*(.*)\s*|'
	pattern = '.*<(.*)>.*(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}).*'
	
	history = rdf.queryDatabaseHttp(query)
	
	resource = None
	timestamp = None
	dictionary = None
	
	html = buildHeader()
	
	historyArray = re.split("\n", history)
	
	for line in historyArray:

		matchObj = re.match(pattern, line)
		if matchObj:
			resource = matchObj.group(1)
			timestamp = matchObj.group(2)
			#print str(timestamp) + " : " + str(resource)
			tempDict = { timestamp : resource}
			if not dictionary:
				dictionary = tempDict
			else:
				dictionary.update(tempDict)

	for key in sorted(dictionary.iterkeys(), reverse = True):
		#print key + "\t" + dictionary[key]
		html += "<p>" + key + " : <a href=\"" + dictionary[key] + "\">" + dictionary[key] + "</a></p>\n"
	
	html += buildFooter()
	
	return html

getHistory()
