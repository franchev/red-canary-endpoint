import logging
import platform
from PlatformEndpoint import *
import argparse


class Endpoint:
    """ Class to gather endpoint activity across different platforms
    """
    platformObject = ""
    def __init__(self):
        pass

    def setPlatformObject(self, logger, handler):
        self.platformObject = PlatformEndpoint(logger, handler)
        self.logger = logger
        self.handler = handler

    def getArgs(self, argv=None):
        parser = argparse.ArgumentParser(description="Red Canary Endpoint")
        parser.add_argument("start_process", type=str, help="start A process. Takes subarguments")
        return parser.parse_args(argv)

    def createLogger(self):
        logFormatter = logging.Formatter("%(asctime)s - %(message)s")

        # configure file handler
        fileHandler = logging.FileHandler('file.log')
        fileHandler.setFormatter(logFormatter)

        logger = logging.getLogger(__name__)

        logger.setLevel(logging.INFO)

        logger.addHandler(fileHandler)
        return logger, fileHandler

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
            logger.warning("your descriptor %s does not exist, please either provide create, modify or delete as a descriptor" % descriptor)

    def start_connections(self, host, port, data, num_conns=1):
        self.platformObject.transmitData(host, port, num_conns, data)


# beginning of program
if __name__ == "__main__":
    # create endpoint object
    endpoint = Endpoint()

    # create logger
    print "going to create logger"
    logger, handler = endpoint.createLogger()

    # set platformEndpoint object
    endpoint.setPlatformObject(logger, handler)

    # testing starting a process
    #endpoint.startProcess("python")

    # testing creating a file
    endpoint.fileManipulator("create", "/Users/francescakoulikov/red-canary", "test.txt")

    # testing deleting a file
    endpoint.fileManipulator("modify", "/Users/francescakoulikov/red-canary", "test.txt", data="what am I to do")


