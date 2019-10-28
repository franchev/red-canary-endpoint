import logging
import platform
from PlatformEndpoint import *
import argparse


class Endpoint:
    """ Class to gather endpoint activity across different platforms
    """
    platformObject = ""
    def __init__(self):
        self.platformObject = PlatformEndpoint()

    def getArgs(self, argv=None):
        parser = argparse.ArgumentParser(description="Red Canary Endpoint")
        parser.add_argument("start_process", type=str, help="start A process. Takes subarguments")
        return parser.parse_args(argv)

    def createLogger(self):
        logger = logging.getLogger(__name__)
        
        # Create handlers
        handler = logging.FileHandler('file.log')
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def setLoggingFormatter(self, logger, formatter):
        handler = logging.FileHandler('file.log')
        handler.setFormatter(formatter)
        logger.addHandler(handler)


    def startProcess(self, logger, processName, processCommand=None):
        # creating a custom logger
        self.platformObject.startAProcess(processName, logger, processCommand)

    def fileManipulator(self, descriptor, filePath, filename, logger):
        if descriptor.lower() == "create":
            self.platformObject.createAFile(filePath, filename, logger)
        elif descriptor.lower() == "modify":
            self.platformObject.modifyAFile(filePath, filename, logger, data="hello world")
        elif descriptor.lower() == "delete":
            self.platformObject.deleteAFile(filePath, filename, logger)
        else:
            logger.warning("your descriptor %s does not exist, please either provide create, modify or delete as a descriptor" % descriptor)


    def establishNetworkConnection(self):
        pass

    def transmitData(self):
        pass


# beginning of program
if __name__ == "__main__":
    # create endpoint object
    endpoint = Endpoint()

    # create logger
    print "going to create logger"
    logger = endpoint.createLogger()

    # testing starting a process
    endpoint.startProcess(logger, "python") 


