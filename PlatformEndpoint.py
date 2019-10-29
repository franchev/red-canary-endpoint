import platform
import subprocess
import logging
import os
import getpass

class PlatformEndpoint():
    runningPlatform = ""

    def __init__(self, logger, handler):
        self.runningPlatform = platform.system()
        self.logger = logger
        self.handler= handler 

    def startAProcess(self, processName, processCommand=None):
        process = None
        try:
            if self.runningPlatform.lower() == "windows":
                if processCommand:
                    process = subprocess.Popen([r'"%s" %s' % (processName, processCommand)], shell=False)
                    self.setLoggerFormatter(process=process, processName=processName, processCommand=processCommand)
                    self.logger.info("Create %s process %s" % (self.runningPlatform, processName))
                else:
                    process = subprocess.Popen([r'"%s"' % (processName)], shell=False)
                    self.setLoggerFormatter(process=process, processName=processName)
                    self.logger.info("Create %s process %s" % (self.runningPlatform, processName))
            if self.runningPlatform.lower() == "linux" or self.runningPlatform.lower() == "darwin":
                if processCommand:
                    process = subprocess.Popen(["%s, %s" % (processName, processCommand)], shell=False)
                    self.setLoggerFormatter(process=process, processName=processName, processCommand=processCommand)
                    self.logger.info("Create %s process %s" % (self.runningPlatform, processName))
                else:
                    process = subprocess.Popen(["%s" % processName], shell=False)
                    self.setLoggerFormatter(process=process, processName=processName)
                    self.logger.info("Create %s process %s" % (self.runningPlatform, processName))
        except Exception as e:
            self.logger.error("Could not start process %s, error %s" % (processName, str(e)))

    def setLoggerFormatter(self, process=None, processName="python", processCommand="None", extraParameters=None):
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
                                                                     extraFormatterString['sourceAddress'], extraParameters['sourcePort'],
                                                                     extraParameters['amount'], extraParameters['protocol'])
                formatter = logging.Formatter('%(asctime)s ' + extraFormatterString + defaultFormatterString + ' message: %(message)s')
        else:
            formatter = logging.Formatter('%(asctime)s ' + defaultFormatterString + ' message: %(message)s')
        self.handler.setFormatter(formatter)

    def createAFile(self, filepath, filename):
        try:
            open("%s/%s" % (filepath, filename), 'a').close()
            loggerDict={'descriptor': 'create', 'fullPath': "%s/%s" % (filepath, filename), 'action': 'fileManipulation' }
            self.setLoggerFormatter(extraParameters=loggerDict)
            self.logger.info("Create file %s/%s " % (filepath, filename))
        except OSError as e:
            if e.errno != errno.ENOENT:
                self.logger.error("cannot create file %s/%s because of error %s" % (filepath, filename, e))
            else:
                self.logger.warning("Error creating file %s/%s because of error %s" % (filepath, filepath, e))

    def modifyAFile(self, filepath, filename, data, action="append"):
        try:
            loggerDict={'descriptor': 'modify', 'fullPath': "%s/%s" % (filepath, filename), 'action': 'fileManipulation' }
            self.setLoggerFormatter(extraParameters=loggerDict)
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
            self.setLoggerFormatter(extraParameters=loggerDict)
            os.remove("%s/%s" % (filepath, filename))
            self.logger.info = "Deleted file %s/%s " % (filepath, filename)
        except Exception as e:
                self.logger.error= "an error occurred, while deleting file %s/%s. error: %s" % (filepath, filename, str(e))
    
    def transmitData(self, host, port, data, num_conns = 1):
        try:
            transmitDataDict={ 'destinationAdress': "blah",
                               'destinationPort': 1433,
                               'sourceAddress': "blah",
                               'sourcePort': 1433,
                               'amount': 23,
                               'protocol': 'tcp',
                               'action': 'network' 
            }
            self.setLoggerFormatter(extraParameters=transmitDataDict)
            self.logger.Info("transmitted data")
            for i in range(0, num_conns):
                connid = i + 1
                print('starting connection', connid, 'to', server_addr)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.setblocking(False)
                sock.connect_ex(server_addr)
                events = selectors.EVENT_READ | selectors.EVENT_WRITE
                data = types.SimpleNamespace(connid=connid,
                                             msg_total=sum(len(m) for m in messages),
                                             recv_total=0,
                                             messages=list(messages),
                                             outb=b'')
                sel.register(sock, events, data=data)
        except Exception as e:
            self.logger.ERROR("cannot transmit data. Review error: %s" % str(e))