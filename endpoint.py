import logging
import platform
import PlatformEndpoint
import DataTransmitter
import LoggerProvider
import argparse
import socket
from PlatformEndpoint import *
from DataTransmitter import *
from LoggerProvider import *


class Endpoint:
    """ Class to gather endpoint activity across different platforms
    """
    platformObject = ""
    def __init__(self):
        pass

    def setLogger(self):
        self.loggerObject = LoggerProvider()
        self.logger, self.handler = self.loggerObject.createLogger()

    def setPlatformObject(self):
        self.platformObject = PlatformEndpoint(self.loggerObject, self.logger, self.handler)

    def getArgs(self, argv=None):
        parser = argparse.ArgumentParser(description="Red Canary Endpoint")
        parser.add_argument("start_process", type=str, help="start A process. Takes subarguments")
        return parser.parse_args(argv)


    def startProcess(self, processName, processCommand=None):
        # creating a custom logger
        self.platformObject.startAProcess(processName, processCommand)

    def fileManipulator(self, descriptor, filePath, filename, data="hello world"):
        if descriptor.lower() == "create":
            self.platformObject.createAFile(filePath, filename)
        elif descriptor.lower() == "modify":
            self.platformObject.modifyAFile(filePath, filename, data="hello world")
        elif descriptor.lower() == "delete":
            self.platformObject.deleteAFile(filePath, filename)
        else:
            self.logger.warning("your descriptor %s does not exist, please either provide create, modify or delete as a descriptor" % descriptor)

    def transmitData(self, host, port, data, protocol='tcp'):
        # DataTransmitter object
        msgLen = len(data)
        sourceHostName = socket.gethostbyname()
        sourceHost = socket.gethostbyname(sourceHostName)
        dataTransmissionCustomFormatterDict = {
            'destinationAddress': host,
            'destinationPort': port,
            'sourceAddress': sourceHost,
            'sourcePort': None,
            'protocol': protocol,
            'amount': msgLen,
            'action': 'network'
        }
        self.loggerObject.setCustomLoggerFormatter(extraParameters=dataTransmissionCustomFormatterDict)
        dataTransmitterObject = DataTransmitter(host, port, self.logger)
        socket = dataTransmitterObject.setSock()
        sourceHost, sourcePort = socket.getsockname()
        dataTransmissionCustomFormatterDict['sourcePort'] = sourcePort
        self.loggerObject.setCustomLoggerFormatter(extraParameters=dataTransmissionCustomFormatterDict)
        dataTransmitterObject.connect()
    
# beginning of program
if __name__ == "__main__":
    # create endpoint object
    endpoint = Endpoint()

    # create logger
    endpoint.setLogger()

    # set platformEndpoint object
    #endpoint.setPlatformObject(logger, handler)

    # testing starting a process
    #endpoint.startProcess("python")

    # testing creating a file
    #endpoint.fileManipulator("create", "/Users/francescakoulikov/red-canary", "test.txt")

    # testing deleting a file
    #endpoint.fileManipulator("modify", "/Users/francescakoulikov/red-canary", "test.txt", data="what am I to do")

    # Testing transmitting data
    host = "https://postman-echo.com/post"
    port = 443
    data = [b'Message 1 from frany.', b'Message 2 from frany.']
    endpoint.transmitData(host, port, data)

