import json
import os.path

class Data():
    def __init__(self,fileName,dirName):
        self.fileName = fileName
        print(self.fileName)
        self.dirname = dirName
        self.data = self.openjson()

    def filecheck(self):
        file = os.path.isfile(self.fileName)
        print(file)
        if not file:
            open(self.fileName,"x")
            self.writejson({self.dirname:[]})
            return False
        else:
            return True
        
    def openjson(self):
        self.filecheck()
        with open(self.fileName) as json_file:
            return json.load(json_file)
    
    def writejson(self,jsonData):
        with open(self.fileName, 'w') as outfile:
            json.dump(jsonData, outfile)
    
    def getjson():
        return self.data
    
    def addjson(item,data):
        for i in self.data[self.dirname]:
            if i[item] == data[item]:
                i = data
                return True
        return false



Data("config.json","Kamers")