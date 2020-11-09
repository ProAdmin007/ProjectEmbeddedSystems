import json
import os.path
import serial

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

    def connector(self, comport):
        # open connectie op poort COMport
        self.ser = serial.Serial(comport, 9600,timeout=10)

    def bereken(self):
        # infenent loop to read data
        while True:
            # read the first command
            # leest het eerste bit
            # 0x41 => next byte is distance data
            # 0x4C => next byte is light data
            # 0x54 => next byte is temp data
            command = self.ser.read().hex()
            if command == '41':
                dist_data = self.ser.read().hex()
                dist_dec = int(dist_data, 16)
                #print('distance - 0x{}'.format(dist_data))
                print('Distance in decimaal = ',dist_dec)
                return dist_dec
            if command == '4c':
                light_data = self.ser.read().hex()
                light_dec = int(light_data, 16)
                #print('light - 0x{}'.format(light_data))
                print('Light in decimaal = ',light_dec)
                return light_dec
            if command == '54':
                temp_data = self.ser.read().hex()
                voltageOut = (int(temp_data, 16) * 5000) / 1024
                temperatureC = round((voltageOut / 10) * 4)
                #print('temp - 0x{}'.format(temp_data))
                print('Temp in C = ',temperatureC)
                return temperatureC

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
