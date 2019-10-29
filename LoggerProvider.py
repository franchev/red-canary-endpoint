import logging
import os
import getpass

class LoggerProvider:
    ''' Class to set Logger '''
    def createLogger(self):
        '''
        Method to create a logger 

        Args: None
        Returns:
            loggingObject: logger
            loggingHandler: filehandler
        '''
        defaultLogFormatter = logging.Formatter("%(asctime)s - %(message)s")

        # configure file handler
        fileHandler = logging.FileHandler('file.log')
        fileHandler.setFormatter(defaultLogFormatter)

        logger = logging.getLogger(__name__)

        logger.setLevel(logging.INFO)

        logger.addHandler(fileHandler)
        self.logger = logger
        self.handler = fileHandler
        return logger, fileHandler


    def setCustomLoggerFormatter(self, process=None, processName="python", processCommand="None", extraParameters=None):
        '''
        Method to set custom logger formatter depending on the action taken place

        Args:
            param1: process (optional)
            param2: processName (optional)
            param3: processCommand (optional)
            param4: extraParameters (optional)

        Returns: None
        '''
        if process:
            processId = str(process.pid)
        else:
            processId = os.getpid()
        username = getpass.getuser()
        defaultFormatterString = " username: %s - process name: %s - process command: %s - process Id: %s " % (username, 
                                                         processName, processCommand, processId)
        if extraParameters:
            if extraParameters['action'].lower() == 'filemanipulation':
                extraFormatterString = "fullPath: %s - activity descriptor: %s " % (extraParameters['fullPath'], extraParameters['descriptor']) 
                formatter = logging.Formatter('%(asctime)s ' + extraFormatterString + defaultFormatterString + ' message: %(message)s')
            elif extraParameters['action'].lower() == 'network':
                extraFormatterString = "destination address/port: %s/%s - source address/port: %s/%s - amount of data send %d - \
                                       protocol of data sent: %s" % (extraParameters['destinationAddress'], extraParameters['destinationPort'],
                                                                     extraParameters['sourceAddress'], extraParameters['sourcePort'],
                                                                     extraParameters['amount'], extraParameters['protocol'])
                formatter = logging.Formatter('%(asctime)s ' + extraFormatterString + defaultFormatterString + ' message: %(message)s')
        else:
            formatter = logging.Formatter('%(asctime)s ' + defaultFormatterString + ' message: %(message)s')
        self.handler.setFormatter(formatter)