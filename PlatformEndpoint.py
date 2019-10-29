import platform
import subprocess
import logging
import os
import getpass

class PlatformEndpoint():
    runningPlatform = ""

    def __init__(self, loggerObject, logger, handler):
        self.runningPlatform = platform.system()
        self.loggerObject = loggerObject
        self.logger = logger
        self.handler= handler 

    def startAProcess(self, processName, processCommand=None):
        '''
        Method to start a process
        Args:
          param1: processName
          param2: processCommand (optional)
        
        Returns: None
        '''
        process = None
        try:
            if self.runningPlatform.lower() == "windows":
                if processCommand:
                    process = subprocess.Popen([r'"%s" %s' % (processName, processCommand)], shell=False)
                    self.loggerObject.setCustomLoggerFormatter(process=process, processName=processName, processCommand=processCommand)
                    self.logger.info("Create %s process %s" % (self.runningPlatform, processName))
                else:
                    process = subprocess.Popen([r'"%s"' % (processName)], shell=False)
                    self.loggerObject.setCustomLoggerFormatter(process=process, processName=processName)
                    self.logger.info("Create %s process %s" % (self.runningPlatform, processName))
            if self.runningPlatform.lower() == "linux" or self.runningPlatform.lower() == "darwin":
                if processCommand:
                    process = subprocess.Popen(["%s, %s" % (processName, processCommand)], shell=False)
                    self.loggerObject.setCustomLoggerFormatter(process=process, processName=processName, processCommand=processCommand)
                    self.logger.info("Create %s process %s" % (self.runningPlatform, processName))
                else:
                    process = subprocess.Popen(["%s" % processName], shell=False)
                    self.loggerObject.setCustomLoggerFormatter(process=process, processName=processName)
                    self.logger.info("Create %s process %s" % (self.runningPlatform, processName))
        except Exception as e:
            self.logger.error("Could not start process %s, error %s" % (processName, str(e)))


    def createAFile(self, filepath):
        '''
        Method to create a file

        Args:
            param1: filepath
        
        Returns: None
        '''
        try:
            open("%s" % filepath, 'a').close()
            loggerDict={'descriptor': 'create', 'fullPath': "%s" % filepath, 'action': 'fileManipulation' }
            self.loggerObject.setCustomLoggerFormatter(extraParameters=loggerDict)
            self.logger.info("Create file %s " % filepath)
        except OSError as e:
            if e.errno != os.errno.ENOENT:
                self.logger.error("cannot create file %s because of error %s" % (filepath, e))
            else:
                self.logger.warning("Error creating file %s because of error %s" % (filepath, e))

    def modifyAFile(self, filepath, data, action="append"):
        '''
        Method to modify a file

        Args:
            param1: filepath
            param2: data
            param3: action
        
        Returns: None
        '''
        try:
            loggerDict={'descriptor': 'modify', 'fullPath': "%s" % filepath, 'action': 'fileManipulation' }
            self.loggerObject.setCustomLoggerFormatter(extraParameters=loggerDict)
            if action.lower == "prepend":
                with open("%s" % filepath, "r+") as fileToModify:
                    oldState = fileToModify.read()
                    fileToModify.seek(0)
                    fileToModify.write(data + oldState)
                    self.logger.info("added data to file %s" % filepath)
            else:
                with open("%s" %filepath, "a+") as fileToModify:
                    fileToModify.write(data)
                    self.logger.info("added data to file %s" % filepath)
        except Exception as e:
            self.logger.error("Error while modifying file %s. Error %s" % (filepath, str(e)))
            


    def deleteAFile(self, filepath):
        '''
        Method to delete a file
        
        Args:
            param1: filepath

        Returns: None
        '''
        try:
            loggerDict={'descriptor': 'delete', 'fullPath': "%s" % filepath, 'action': 'fileManipulation' }
            self.loggerObject.setCustomLoggerFormatter(extraParameters=loggerDict)
            os.remove("%s" % filepath)
            self.logger.info = "Deleted file %s " % filepath
        except Exception as e:
                self.logger.error= "an error occurred, while deleting file %s. error: %s" % (filepath, str(e))
    