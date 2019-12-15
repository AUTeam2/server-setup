__VERSION__ = "1.0"
import json

class Payload():

    #Attributes
    protocolVersion = __VERSION__
    sentBy = str()
    msgType = str()
    commandList = list()
    statusCode = str()
    parameterObj = dict()
    dataObj = dict()
    embeddedFileFormat = str()
    embeddedFile = str()

    _payload_prototype = {
        "protocolVersion": __VERSION__,
        "sentBy": "",
        "msgType": "",
        "commandList": "",
        "statusCode": "",
        "parameterObj": "",                 #
        "dataObj": "",                      # JSON schema for results for the testStand
        "embeddedFileFormat": "",           # formatType
        "embeddedFile": "",                 # binary file data
    }

    def __init__(self):
        self.value = self._payload_prototype    # Initialize with the protocol format
        self.message = json.dumps(self.value)

    def validate(self):
        return True

    def pack(self):

        if not self.validate():
            raise RuntimeError

        #go from attributes to dict
        self.value.update(
            protocolVersion=self.protocolVersion,
            sentBy=self.sentBy,
            msgType=self.msgType,
            commandList=self.commandList,
            statusCode=self.statusCode,
            parameterObj=self.parameterObj,
            dataObj=self.dataObj,
            embeddedFileFormat=self.embeddedFileFormat,
            embeddedFile=self.embeddedFile,
        )

        #pack the dict into a json string
        self.message = json.dumps(self.value)

    def unpack(self):
        #unpack JSON to a dict
        print("2!")
        print(self.message)
        self.value = json.loads(self.message)

        print("3!")
        #do the reverse setting from dict to attributes
        self.protocolVersion = self.value["protocolVersion"]
        self.sentBy = self.value["sentBy"]
        self.msgType = self.value["msgType"]
        self.commandList = self.value["commandList"]
        print("4!")
        self.statusCode = self.value["statusCode"]
        self.parameterObj = self.value["parameterObj"]
        self.dataObj = self.value["dataObj"]
        self.embeddedFileFormat = self.value["embeddedFileFormat"]
        self.embeddedFile = self.value["embeddedFile"]

    def reset(self):
        self.__init__(self)