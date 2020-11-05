import json
import os.path

class Main():
    def __init__(self,fileName):
        self.data = self.openjson(fileName)

    def filecheck(self,fileName):
        file = os.path.isfile(fileName)
        if not file:
            open(fileName,"x")
            self.writejson(fileName,{"Kamers":[]})
            return False
        else:
            return True
        
    def openjson(self,fileName):
        self.filecheck(fileName)
        with open(fileName) as json_file:
            return json.load(json_file)
    
    def writejson(self,fileName,jsonData):
        with open(fileName, 'w') as outfile:
            json.dump(jsonData, outfile)
    
Main("test.json")