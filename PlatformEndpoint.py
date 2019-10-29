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


    def createAFile(self, filepath, filename):
        try:
            open("%s/%s" % (filepath, filename), 'a').close()
            loggerDict={'descriptor': 'create', 'fullPath': "%s/%s" % (filepath, filename), 'action': 'fileManipulation' }
            self.loggerObject.setCustomLoggerFormatter(extraParameters=loggerDict)
            self.logger.info("Create file %s/%s " % (filepath, filename))
        except OSError as e:
            if e.errno != os.errno.ENOENT:
                self.logger.error("cannot create file %s/%s because of error %s" % (filepath, filename, e))
            else:
                self.logger.warning("Error creating file %s/%s because of error %s" % (filepath, filepath, e))

    def modifyAFile(self, filepath, filename, data, action="append"):
        try:
            loggerDict={'descriptor': 'modify', 'fullPath': "%s/%s" % (filepath, filename), 'action': 'fileManipulation' }
            self.loggerObject.setCustomLoggerFormatter(extraParameters=loggerDict)
            if action.lower == "prepend":
                with open("%s/%s" % (filepath, filename), "r+") as fileToModify:
                    oldState = fileToModify.read()
                    fileToModify.seek(0)
                    fileToModify.write(data + oldState)
                    self.logger.info("added data to file %s/%s" % (filepath, filename))
            else:
                with open("%s/%s" %(filepath, filename), "a+") as fileToModify:
                    fileToModify.write(data)
                    self.logger.info("added data to file %s/%s" % (filepath, filename))
        except Exception as e:
            self.logger.error("Error while modifying file %s/%s. Error %s" % (filepath, filename, str(e)))
            


    def deleteAFile(self, filepath, filename):
        try:
            loggerDict={'descriptor': 'delete', 'fullPath': "%s/%s" % (filepath, filename), 'action': 'fileManipulation' }
            self.loggerObject.setCustomLoggerFormatter(extraParameters=loggerDict)
            os.remove("%s/%s" % (filepath, filename))
            self.logger.info = "Deleted file %s/%s " % (filepath, filename)
        except Exception as e:
                self.logger.error= "an error occurred, while deleting file %s/%s. error: %s" % (filepath, filename, str(e))
    