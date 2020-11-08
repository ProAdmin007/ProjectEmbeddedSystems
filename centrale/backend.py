import json
import os.path

class Data():
    def __init__(self, fileName, dirName):
        self.fileName = fileName
        self.dirname = dirName
        self.data = self.openjson()

    def filecheck(self):
        file = os.path.isfile(self.fileName)
        if not file:
            open(self.fileName, "x")
            self.writejson({self.dirname: {}})
            return False
        else:
            return True

    def openjson(self):
        self.filecheck()
        with open(self.fileName) as json_file:
            return json.load(json_file)

    def writejson(self, jsonData):
        with open(self.fileName, 'w') as outfile:
            json.dump(jsonData, outfile)

    def getjson(self):
        self.data = self.openjson()
        return self.data

# test =Data ("config.json","Kamers")
# testdata = test.getjson()
# testdata["Kamers"]["kamernummer4"] = {"com":[]}
# testdata["Kamers"]["kamernummer7"] = {"com":[]}
# testdata["Kamers"]["kamernummer1"] = {"com":[]}
# print(testdata)
# test.writejson(testdata)


# eerste = testdata["kamer1"] = {}
# tweede = testdata["kamer2"] = {}
# eerste["naam"] = "kamernaam1"
# tweede["naam"] = "kamernaam2"
# eerste["schermen"] = ["com1","com2"]
# tweede["schermen"] = ["com3","com4"]
# jsonator["Kamers"] = [eerste]
# jsonator["Kamers"] += [tweede]
# test.writejson(jsonator)
