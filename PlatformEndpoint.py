import platform
import subprocess
import logging
import os

class PlatformEndpoint():
    runningPlatform = ""

    def __init__(self):
        self.runningPlatform = platform.system()

    def startAProcess(self, processName, processLogger, processCommand=None):
        try:
            if self.runningPlatform.lower() == "windows":
                if processCommand:
                    process = subprocess.Popen([r'"%s" %s' % (processName, processCommand)], shell=False)
                    processLogger = self.setLoggerFormatter(process, processLogger)
                    processLogger.info("Create %s process %s" % (self.runningPlatform, processName))
                else:
                    process = subprocess.Popen([r'"%s"' % (processName)], shell=False)
                    processLogger = self.setLoggerFormatter(process, processLogger)
                    processLogger.info("Create %s process %s" % (self.runningPlatform, processName))
            if self.runningPlatform.lower() == "linux" or self.runningPlatform.lower() == "darwin":
                if processCommand:
                    process = subprocess.Popen(["%s, %s" % (processName, processCommand)], shell=False)
                    processLogger = self.setLoggerFormatter(process, processLogger)
                    processLogger.info("Create %s process %s" % (self.runningPlatform, processName))
                else:
                    process = subprocess.Popen(["%s" % processName], shell=False)
                    processLogger = self.setLoggerFormatter(process, processLogger)
                    processLogger.info("Create %s process %s" % (self.runningPlatform, processName))
            processLogger.info("started process")
        except Exception as e:
            processLogger.error("Could not start process %s, error %s" % (processName, e))

    def setLoggerFormatter(self, process, logger):
        processId = str(process.pid)
        username = str(process)
        processName = "python"
        processCommand = "python2" 
        formatterLogging = "%s - %s - %s - %s" % (username, processName, processCommand, processId)
        handler = logging.FileHandler('file.log')
        handler.setFormatter(formatterLogging)
        logger.addHandler(handler)
        logger.Handler.setformatter(formatterLogging)
        return logger

    def createAFile(self, filepath, filename, createFileLogger):
        try:
            open("%s/%s" % (filepath, filename), 'a').close()
            process = ""
            createFileLogger = self.setLoggerFormatter(process, createFileLogger)
            createFileLogger.info("Create file %s/%s " % (filepath, filename))
        except OSError as e:
            if e.errno != errno.ENOENT:
                createFileLogger.error("cannot create file %s/%s because of error %s" % (filepath, filename, e))
            else:
                createFileLogger.warning("Error creating file %s/%s because of error %s" % (filepath, filepath, e))

    def modifyAFile(self, filepath, filename, modifyFileLogger, data, action="append"):
        try:
            process = ""
            modifyFileLogger = self.setLoggerFormatter(process, modifyFileLogger)
            if action.lower == "prepend":
                with open("%s/%s", "r+") as fileToModify:
                    oldState = fileToModify.read()
                    fileToModify.seek(0)
                    fileToModify.write(data + oldState)
                    modifyFileLogger.info("added data to file %s/%s" % (filepath, filename))
            else:
                with open("%s/%s", "a") as fileToModify:
                    fileToModify.write(data)
                    modifyFileLogger.info("added data to file %s/%s" % (filepath, filename))
        except Exception as e:
            modifyFileLogger.error("Error while modifying file %s/%s. Error %s" % (filepath, filename, e))
            


    def deleteAFile(self, filepath, filename, deleteFileLogger):
        try:
            os.remove(filepath/filename)
            deleteFileLogger.info = "Deleted file %s/%s " % (filepath, filename)
        except OSError as e:
            if e.errno != errno.ENOENT:
                deleteFileLogger.error= "an error occurred"
            else:
                deleteFileLogger.info = "File %s/%s does not exist" % (filepath, filename)
                