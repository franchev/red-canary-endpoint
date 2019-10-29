import sys

class ArgParseProvider:
    """ Class to get & set arguments and subarguments from user """

    def printhelpArgs(self):
        helpMessage = """
        endpoint - redcanary endpoint program
        Usage: endpoint [options] [suboptions]

            this endpoint program is to do these actions:
            process -> to start a process
            file -> to manipulate a file (create, delete, modify)
            transmit -> to transmit data

            options:
            help: will reprint this print statement
            process: start a process
               suboption: 
                   processPath: process path to start
                   processCommand: desired command-line arguments (optional)
            file: manipulate file
               suboption:
                   action: action to perform with file (create, modify, delete)
                   filePath: path where file to be created
                   data: data to be added to file (only if action == modified)
            transmit: data to be transmitted
               suboption:
                   destination address: added of receiving server
                   destination port: port to receive data on
                   data: data to send
                   protocol: protocol to be used (tcp/udp) optional (default tcp)
            
            examples:
               to start a process;
                   python Endpoint.py process [processPath] [processCmdArgs]
               to create a file:
                   python Endpoint.py file create /usr/local/bin/test.txt
               to modify an existing file:
                   python Endpoint.py file modify /usr/local/bin/test.txt "hello world"
               to delete a file:
                   python Endpoint.py file delete /usr/local/bin/test.txt
               to transmit data:
                   python Endpoint.py trasmit 192.168.1.23 443 [b'data1 to send'] 
        """
        print helpMessage
        exit
    
    def setProcessArgs(self, args):
        processPathArg = ""
        processCommandArg = ""
        if len(args) >= 3:
            processPathArg = args[2]
            if len(args) >= 4:
                processCommandArg = args[3]
        else:
            self.printhelpArgs()
        return processPathArg, processCommandArg

    def setFileArgs(self, args):
        filePathArg = ""
        fileAction = ['create', 'delete', 'modify']
        data = ""
        actionToPerform = ""
        if len(args) >= 4:
            actionToPerform = args[2]
            if actionToPerform not in fileAction:
                self.printhelpArgs()
            filePathArg = args[3]
        else:
            self.printhelpArgs()
        
        if actionToPerform.lower() == 'modify':
            if len(args) >= 5:
                data = args[4]
            else:
                self.printhelpArgs()
                exit
        return actionToPerform, filePathArg, data

    def setTransmitArgs(self, args):
        destinationAddressArg = ""
        destinationPortArg = ""
        dataArg = ""
        protocol = "tcp"

        if len(args) >= 5:
            destinationAddressArg = args[2]
            destinationPortArg = args[3]
            dataArg = args[4]

            if len(args) >= 6:
                protocol = args[5]
        else:
            self.printhelpArgs()
        return destinationAddressArg, destinationPortArg, dataArg, protocol 
                 