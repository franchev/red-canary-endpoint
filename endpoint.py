import logging
import platform

class Endpoint:
    """ Class to gather endpoint activity across different platforms
    """


    def __init__(self):
        # Initiate Platform Object to call the process class
        self.setPlatform()

    def createLogger(self, loggingFormat):
        logger = logging.getLogger(__name__)
        
        # Create handlers
        handler = logging.FileHandler('file.log')
        handler.setLevel(logging.INFO)
        format = logging.Formatter(loggingFormat)
        handler.setFormatter(format)
        logger.addHandler(handler)
        return logger

    def setPlatformObject(self):
        """
        simple method to platform object 
        """
        self.platform.object = Platform()


    def startProcess(self):
        # creating a custom logger
        formatterForLogin = "%(asctime)s - %s - %s - %s" % (username, processName, processId)
        processLogger = self.createLogger(formatterForLogin)
        self.platform.object.startAProcess(username, processName, processLogger, command)

    def fileManipulator(self, descriptor, filePath, filename):
        formatterForLogin = "%(asctime)s - %s - %s - %s - %s - %s - %s" % ( filePath, descriptor, 
                                                             username, processName, processCommandLine, processId)
        fileManipulatorLogger = self.createLogger(formatterForLogin)
        if descriptor.lower() == "create":
            self.platform.object.createFile(filePath, filename, fileManipulatorLogger)
        elif descriptor.lower() == "modify":
            self.platform.object.modifyFile(filePath, filename, fileManipulatorLogger)
        elif descriptor.lower() == "delete":
            self.platform.object.deleteFile(filePath, filename, fileManipulatorLogger)
        else:
            processLogger.WARNING("your descriptor %s does not exist, please either provide create, modify or delete as a descriptor" %s descriptor)

  
    def createFile(self, filePath, filename, logger):
        pass

    def modifyFile(self, filePath, filename, logger):
        fullFile = "%s/%s" % (filePath, filename)
        try:
            pass
        except:
            

    def deleteFile(self, filePath, filename, logger):
        try:
            os.remove("%s/%s" % (filePath/filename))
            logger.INFO("Successfully deleted file %s/%s" % (filePath, filename))
        except Exception as error:
            logger.ERROR("Error while deleting file %s/%s" % (filePath, filename))

    def establishNetworkConnection(self):
        formatterForLogin = "%(asctime)s - %s - %s - %s" % (username, processName, processId)
        processLogger = self.createLogger(formatterForLogin)
        pass

    def transmitData(self):
        pass
