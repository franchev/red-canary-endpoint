import platform
import subprocess
import logging

class Platform():
    platform = ""

    def __init__(self):
        platform = platform.system()
        self.platform = platform

    def startAProcess(self, username, processName, processLogger, command=None):
        try:
            if self.platform.lower() == "windows":
                if command:
                    process = subprocess.Popen([r'"%s" %s', % (processName, command)], shell=False)
                else:
                    process = subprocess.Popen([r'"%s"', % processName], shell=False)
            if self.platform.lower() == "linux" or self.platform.lower() == "darwin":
                if command:
                    process = subprocess.Popen(["%s, %s", % (processName, command)], shell=False)
                else:
                    process = subprocess.Popen(["%s", % processName], shell=False)
                    processLogger.INFO("startedProcess")
        except Exception as e:
            processLogger.ERROR("Could not start process")


    def createAFile(self, filepath, filename, createFileLogger):
        try:
            open("%s/%s" % (filepath, filename), 'a').close()
            createFileLogger.INFO("Created file %s/%s" % (filepath, filename))
        except OSError as e:
            if e.errno != errno.ENOENT:
                createFileLogger.ERROR("cannot create file %s/%s because of error %s" % (filepath, filename, e))
            else:
                createFileLogger.WARNING("Error creating file %s/%s because of error %s" % (filepath, filepath, e))

    def modifyAFile(self, filepath, filename, modifyFileLogger, data, action="append"):
        try:
            if action.lower == "prepend":
                with open("%s/%s", "r+") as fileToModify:
                    oldState = fileToModify.read()
                    fileToModify.seek(0)
                    fileToModify.write(data + old)
                    modifyFileLogger.INFO("added data to file %s/%s" % (filepath, filename))
            else:
                with open("%s/%s", "a") as fileToModify:
                    fileToModify.write(data)
                    modifyFileLogger.INFO("added data to file %s/%s" % (filepath, filename))
        except Exception as e:
            modifyFileLogger.ERROR("Error while modifying file %s/%s. Error %s" % (filepath, filename, e))
            


    def deleteAFile(self, filepath, filename, deleteFileLogger):
        try:
            os.remove(filepath/filename)
            deleteFileLogger.INFO = "Deleted file %s/%s " % (filepath, filename)
        except OSError as e:
            if e.errno != errno.ENOENT:
                deleteFileLogger.ERROR= "an error occurred"
            else:
                deleteFileLogger.INFO = "File %s/%s does not exist" % (filepath, filename)
                