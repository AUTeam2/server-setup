"""
This is the implementation of B39, modified slightly for B41.
This module implements functions to load a JSON-schema and validate messages against this schema.
This is an implementation of the protocol v1.0

Contains functions to import a jsonschema,
read/write json files and strings and to validate those.
"""
__VERSION__ = 1.0

import json
import sys
import os
import jsonschema
from jsonschema import validate
from django.conf import settings


# testshcema = {
#     "$schema": "AUTeam2 JSONschema",
#     "title": "PayloadSchema",
#     "type": "object",
#     "properties": {
#         "protocolVersion": {"type": "number"},
#         "sentBy": {"type": "string"},
#         "msgType": {"type": "string"},
#         "commandList": {"type": "string"},
#         "statusCode": {"type": "string"},
#         "parameterObj": {"type": "object"},
#         "dataObj": {"type": "object"},
#         "embeddedFileFormat": {"type": "string"},
#         "embeddedFile": {"type": "string"}
#     },
#     "required": ["protocolVersion", "sentBy", "msgType"]
# }


class ProtocolSchema():

    @staticmethod
    def load_schema(jschema):
        """
        Loads jsonschema from file

        :param jschema:
        Takes a filename as a string
        :return:
        """

        with open(jschema, 'r', encoding="utf-8") as f:
            return json.loads(f.read())

    @staticmethod
    def write_jsonfile(outputfile, data):
        """
        Write "jsonly" correct json files

        :param outputfile:
        Name of the file to be as a string
        :param data:
        Data to be jsonly written in the file
        :return:
        """
        with open(outputfile, 'w', encoding="utf-8") as jsonFile:
            json.dump(data, jsonFile)

    @staticmethod
    def write_jsonstr(var):
        """
        Write "jsonly" correct json string

        :param var:
        :return:
        """
        return json.dumps(var)

    @staticmethod
    def read_jsonstr(var):
        """
        Read json-data from string

        :param var:
        :return:
        """
        return json.loads(var)

    @staticmethod
    def read_jsonfile(inputfile):
        """
        Read json-data from file

        :param inputfile:
        Json file containing data
        :return:
        """
        with open(inputfile, 'r', encoding="utf-8") as datafile:
            return json.load(datafile)

    @staticmethod
    def validating(jsondata, schema):
        """
        Validates json-data against schema

        :param jsondata:
        The variable containing json-data
        :param schema:
        The schema to compare against
        :return:
        """
        #print("Validating the input data using jsonschema:")
        try:
            validate(jsondata, schema)
            #sys.stdout.write("Validation OK\n")
            return True #The validation went well happy happy
        except jsonschema.exceptions.ValidationError as ve:
            print("Timmy says validation baaad mkaayy:")
            sys.stderr.write("Record #{}: ERROR\n".format(jsondata))
            sys.stderr.write(str(ve) + "\n")
            return False #bad! very bad!

    @staticmethod
    def message_is_valid(message, schema):
        """
        EXPERIMENTAL
        Returns true if the message is valid under the given schema
        :param message:
        :param schema:
        :return:
        """
        return jsonschema.Draft3Validator(schema).is_valid(message)



#js = JsonSchemaClass()
#proto = js.load_schema("json.schema")


class Message():
    """
    A message class to handle protocol conforming messages
    """

    def __init__(self):

        #Build a protocol validator
        self.protocol_schema = ProtocolSchema.load_schema(settings.PROTOCOL_SCHEMA_PATH)

        # Extract the payload part, this can be sent when filled
        self.payload = self.protocol_schema["properties"]

    def unpack(self, protocolVersion, sentBy, msgType, commandList, statusCode, parameterObj, dataObj,
               embeddedFileFormat, embeddedFile):
        self.protocolVersion = protocolVersion
        self.sentBy = sentBy
        self.msgType = msgType
        self.commandList = commandList
        self.statusCode = statusCode
        self.parameterObj = parameterObj
        self.dataObj = dataObj
        self.embeddedFileFormat = embeddedFileFormat
        self.embeddedFile = embeddedFile

    def pack(self):
        self.payload["protocolVersion"] = self.protocolVersion
        self.payload["sentBy"] = self.sentBy
        self.payload["msgType"] = self.msgType
        self.payload["commandList"] = self.commandList
        self.payload["statusCode"] = self.statusCode
        self.payload["parameterObj"] = self.parameterObj
        self.payload["dataObj"] = self.dataObj
        self.payload["embeddedFileFormat"] = self.embeddedFileFormat
        self.payload["embeddedFile"] = self.embeddedFile

    def new(self):
        """
        Creates a new or resets the message with empty fields
        :return:
        """
        self.unpack(__VERSION__, "", "", [], "", {}, {}, "", "")