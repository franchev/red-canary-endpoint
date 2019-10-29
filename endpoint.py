import logging
import platform
import PlatformEndpoint
import DataTransmitter
import LoggerProvider
import sys
from PlatformEndpoint import *
from DataTransmitter import *
from LoggerProvider import *
from ArgParseProvider import *


class Endpoint:
    """ Class to gather endpoint activity across different platforms """
    def setLogger(self):
        '''
        Method to set logger

        Args: None
        Returns: None
        '''
        self.loggerObject = LoggerProvider()
        self.logger, self.handler = self.loggerObject.createLogger()

    def setPlatformObject(self):
        '''
        Method to set platform object

        Args: None
        Returns: None
        '''
        self.platformObject = PlatformEndpoint(self.loggerObject, self.logger, self.handler)

    def startProcess(self, processName, processCommand=None):
        '''
        Method to start a process

        Args: 
            param1: processName
            param2: processCommand (optional)
        Returns: None
        '''
        self.platformObject.startAProcess(processName, processCommand)

    def fileManipulator(self, descriptor, fullFilePath, data=""):
        '''
        Method to do file manipulation

        Args:
            param1: descriptor
            param2: fullFilePath
            param3: data (optional)
        Returns: none
        '''
        if descriptor.lower() == "create":
            self.platformObject.createAFile(fullFilePath)
        elif descriptor.lower() == "modify":
            self.platformObject.modifyAFile(fullFilePath, data)
        elif descriptor.lower() == "delete":
            self.platformObject.deleteAFile(fullFilePath)
        else:
            self.logger.warning("your descriptor %s does not exist, please either provide create, modify or delete as a descriptor" % descriptor)

    def transmitData(self, host, port, data, protocol='tcp'):
        '''
        Method to transmit data

        Args:
            param1: host 
            param2: port
            param3: data
            param4: protocol
        
        Returns: None
        '''
        # DataTransmitter object
        msgLen = len(data)
        dataTransmissionCustomFormatterDict = {
            'destinationAddress': host,
            'destinationPort': port,
            'sourceAddress': 'localhost',
            'sourcePort': None,
            'protocol': protocol,
            'amount': msgLen,
            'action': 'network'
        }
        self.loggerObject.setCustomLoggerFormatter(extraParameters=dataTransmissionCustomFormatterDict)
        dataTransmitterObject = DataTransmitter(host, port, self.logger)
        socket = dataTransmitterObject.setSock()
        sourceHost, sourcePort = socket.getsockname()
        dataTransmissionCustomFormatterDict['sourceHost'] = sourceHost
        dataTransmissionCustomFormatterDict['sourcePort'] = sourcePort
        self.loggerObject.setCustomLoggerFormatter(extraParameters=dataTransmissionCustomFormatterDict)
        dataTransmitterObject.connect()
    
# beginning of program
if __name__ == "__main__":
    # create endpoint object
    endpoint = Endpoint()
    
    # create logger
    endpoint.setLogger()

    # create platform object
    endpoint.setPlatformObject()

    # create ArgParseProvider object
    argparseProvider = ArgParseProvider()

    # getting arguments from users and operating as such
    if len(sys.argv) <= 1 or sys.argv[1].lower() == 'help':
       argparseProvider.printhelpArgs()
    else:
        if sys.argv[1].lower() == 'process':
            processPath, processCMD = argparseProvider.setProcessArgs(sys.argv)
            endpoint.startProcess(processPath, processCMD) if processCMD else endpoint.startProcess(processPath)    
        elif sys.argv[1].lower() == 'file':
            action, filePath, data = argparseProvider.setFileArgs(sys.argv)
            endpoint.fileManipulator(action, filePath, data)
        elif sys.argv[1].lower() == 'transmit':
            destinationAddress, destinationPort, dataToTransmit, protocol = argparseProvider.setTransmitArgs(sys.argv)
            endpoint.transmitData(destinationAddress, destinationPort, dataToTransmit, protocol)
        else:
            argparseProvider.printhelpArgs()