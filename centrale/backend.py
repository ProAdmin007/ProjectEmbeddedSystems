import json
import os.path

class main():
    def __init__(self,filename):
        self.data = openjson(self,filename)

    def filecheck(filename):
        file = os.path.isfile(name)
        if file:
            open(name,"x")
            return False
        else:
            return True
        
    def openjson(filename):
        filecheck(filename)
        with open(filename) as json_file:
            return json.load(json_file)
    
    def writejson(filename):
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)
    