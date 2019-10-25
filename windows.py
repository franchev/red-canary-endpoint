import logging

class Endpoint:
    """ Class to gather enpoint activity across different platforms
    """

    def __init__(self):
        pass


    def createLogger(self):
        logger = logging.getLogger(__name__)
        
        # Create handlers
        handler = logging.FileHandler('file.log')
        handler.setLevel(logging.INFO)
        format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(format)
        logger.addHandler(handler)
        return logger

    def getPlatform(self):
        pass

    def startProcess(self):
        # creating a custom logger

        pass

    def createFile(self):
        pass

    def modifyFile(self):
        pass

    def deleteFile(self):
        pass

    def establishNetworkConnection(self):
        pass

    def transmitData(self):
        pass
