import os
import subprocess
from logging_wrapper import info
import time

DBNAME = "xml"


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


def connectDatabase():
        output = subprocess.call(["4s-backend",DBNAME])
        if output == 0:
                info("connected to"+DBNAME+"\n")
                return True
        else:
                info("failure: already connected to"+DBNAME+"\n")
                return False


def disconnectDatabase():
        disconnectStr = '^4s-backend '+DBNAME+'$'
        output = subprocess.call(["pkill","-f",disconnectStr ])
        if output == 0:
                info("disconnected from"+DBNAME+"\n")
        else:
                info("failure: already disconnected to"+DBNAME+"\n")


def importDatasetsFile(file):
        output = subprocess.call(["4s-import",DBNAME,file])
        if output == 0:
                info("data is added\n")
        else:
                info("failure: not able to add data\n")


def importDatasets(data):
        temp_file = str(time.time()) + "data.rdf"
        f = open(temp_file, "w")
        f.write(data)
        f.flush()
        f.close()
        
        importDatasetsFile(temp_file)
        
        if os.path.isfile(temp_file):
            os.remove(temp_file)


def queryDatabase(query):
        output = subprocess.check_output(["4s-query",DBNAME,query])
        return output
