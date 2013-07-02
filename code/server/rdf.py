import os
import subprocess
from logging_wrapper import info
import time

DBNAME = "xml"
PORT = 8000


def createDatabase():
        output = subprocess.call(["4s-backend-setup",DBNAME])
        if output == 0:
                info(DBNAME+" is created\n")
        else:
                info("failure: "+DBNAME+" not created\n")


def deleteDatabase():
        output = subprocess.call(["4s-backend-destroy",DBNAME])
        if output == 0:
                info(DBNAME+" is deleted\n")
        else:
                info("failure: "+DBNAME+" not deleted\n")


def connectDatabaseHttp():
	#output = subprocess.call(["4s-httpd","-p " + str(PORT),DBNAME])
	output = subprocess.call("4s-httpd -X -p " + str(PORT) + " " + DBNAME + " > /dev/null 2>&1", shell=True)
        if output == 0:
                info("connected to"+DBNAME+"\n")
                return True
        else:
                info("failure: already connected to "+DBNAME+"\n")
                return False

def connectDatabase():
        output = subprocess.call(["4s-backend",DBNAME])
        if output == 0:
                info("connected to"+DBNAME+"\n")
                return True
        else:
                info("failure: already connected to "+DBNAME+"\n")
                return False

def disconnectDatabaseHttp():
        output = subprocess.call(["pkill","4s-httpd"])
        if output == 0:
                info("disconnected from"+DBNAME+"\n")
        else:
                info("failure: already disconnected to "+DBNAME+"\n")


def disconnectDatabase():
        disconnectStr = '^4s-backend '+DBNAME+'$'
        output = subprocess.call(["pkill","-f",disconnectStr ])
        if output == 0:
                info("disconnected from"+DBNAME+"\n")
        else:
                info("failure: already disconnected to "+DBNAME+"\n")


def importDatasetsFile(file):
        output = subprocess.call(["4s-import",DBNAME,file])
        if output == 0:
                info("data is added\n")
        else:
                info("failure: not able to add data\n")

def importDatasetsFileHttp(file):
	filename = os.path.split(file)[1]
	hostStr = "'http://localhost:"+str(PORT)+"/data/"+filename+"'"
	#output = subprocess.call(["curl", "-T", file, hostStr])
	curlString = "curl -T " + str(file) + " " + hostStr
	output = subprocess.call(curlString + " > /dev/null 2>&1", shell=True)
        if output == 0:
                info("data is added\n")
        else:
                info("failure: not able to add data: "+str(output)+"\n")
		
	#curl -T out.rdf 'http://localhost:8000/data/out.rdf'


def importDatasets(data):
        temp_file = "data" + str(time.time()) + ".rdf"
        f = open(temp_file, "w")
        f.write(data)
        f.flush()
        f.close()
        
        #importDatasetsFile(temp_file)
        importDatasetsFileHttp(temp_file)
        
        if os.path.isfile(temp_file):
            os.remove(temp_file)

def queryDatabaseHttp(query):
	output = subprocess.check_output(["sparql-query","localhost:"+str(PORT)+"/sparql/",query])
	return output


def queryDatabase(query):
        output = subprocess.check_output(["4s-query",DBNAME,query])
        return output
