import logging
import socket

class DataTransmitter:
    """Class to transmit data"""

    def __init__(self, host, port, logger, protocol='tcp' ):
        self.host = host
        self.port = port
        self.logger = logger
        self.protocol = protocol

    def setSock(self):
        try:
            if self.protocol.lower() == 'udp':
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            else:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.logger.info("setting socket to send data")
        except socket.error as exc:
            self.logger.error("could set socket to send data. Revew error %s" % str(exc))
        return self.sock

    def connect(self):
        try:
            self.sock.connect((self.host, self.port))
            self.logger.info("established connection to send data")
        except socket.error as exc:
            self.logger.error("could not establish connection to send data. Review error %s" % str(exc))

    def sendData(self, msg):
        try:
            MSGLEN = len(msg)
            totalsent = 0
            while totalsent < MSGLEN:
                sent = self.sock.send(msg[totalsent:])
                if sent == 0:
                    raise RuntimeError("socket connection broken")
                totalsent = totalsent + sent
            self.logger.info("send data")
        except socket.error as exc:
            self.logger.error("could not send data. Please review error: %s" % str(exc))