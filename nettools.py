import socket
import sys
import time
from thread import *
#from UserTools import getInput

class peer():
    def __init__(self,Connection,Address):
        self.connection = Connection
        self.address = Address
        print "New client connection created. {}".format(self.address)

    def loopback(self,buffer=1024):
        self.connection.send('Welcome to the party!\r\n')
        while True:
            data = self.connection.recv(buffer)
            #print data
            reply = 'Received: ' + data + '\r\n'
            if not data or data.lower() == 'exit':
                exit() # Stops the thread
                break
            self.connection.send(reply)
        self.connection.close()

    def sendData(self, message,verb=0):
        try:
            self.connection.send(message)
        except socket.error:
            print 'Send failed: {}'.format(socket.error.message)
            self.connection.close()
            sys.exit()
        if verb > 0:
            print 'Message sent successfully'

    def testLoop(self):
        self.connection.send('Welcome to the party!\r\n')
        i = 0
        while True:
            #time.sleep(1)
            i = i + 1
            msg = "Test " + str(i)
            self.connection.send(msg)
            data = self.connection.recv(1024)
            if not data or data.lower() == 'exit':
                exit() # Stops the thread
                break
        self.connection.close()

    def testMessage(self):
        self.connection.send('ABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890')
        self.connection.close()

class node():
    def __init__(self,Hostname):
        self.hostname = Hostname
        self.connected = False
        self.bound = False

    def printIP(self):
        try:
            remote_ip = socket.gethostbyname( self.hostname )
        except socket.gaierror:
            # Could not resolve
            print 'Hostname could not be resolved. Exiting'
            sys.exit()
        print self.hostname + ' resolves to ' + remote_ip

    def getIP(self):
        try:
            remote_ip = socket.gethostbyname( self.hostname )
        except socket.gaierror:
            #could not resolve
            print 'Hostname could not be resolved. Exiting'
            sys.exit()
        return remote_ip

    def connect(self, port=80, verb=0):
        try:
            #create an AF_INET, STREAM socket (TCP)
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
            sys.exit();
        if verb > 0:
            print 'Socket Created'
            print 'Connecting to', self.hostname, 'on port', port
        try:
            hostIP = self.getIP()
            self.socket.connect((self.hostname, port))
            if verb > 0:
                print 'Successfully Connected to ' + self.hostname
                self.connected = True
        except Exception as e:
            self.connected = False
            print 'Failed to connect to ' + self.hostname, e

    def sendData(self, message='GET / HTTP/1.1\r\n\r\n',verb=0):
        try:
            self.socket.sendall(message)
        except socket.error:
            print 'Send failed: {}'.format(socket.error.message)
            sys.exit()
        if verb > 0:
            print 'Message sent successfully'

    def receiveData(self,bufferSize=4096):
        reply = self.socket.recv(bufferSize)
        return reply

    def bind(self, port=8000, verb=0):
        try:
            #create an AF_INET, STREAM socket (TCP)
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
            sys.exit();

        if verb > 0:
            print 'Socket Created'
            print 'Binding to ', self.hostname, 'on port', port
        try:
            self.socket.bind((self.hostname, port))
        except socket.error, msg:
            print 'Bind failed. Error Code: : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()
        if verb > 0:
            print 'Socket Bind Complete.'

if __name__ == "__main__":
    import random
    recvServer = node('192.168.100.249')
    recvServer.bind(42002,verb=10)

    sendServer = node('192.168.100.249')
    sendServer.bind(42001, verb=10)
    sendServer.socket.listen(1)
    con, adr = sendServer.socket.accept()
    sendClient = peer(con, adr)

    recvServer.socket.listen(1)
    con, adr = recvServer.socket.accept()
    recvClient = peer(con,adr)

    count = 0
    while True:
        recvMsg = recvClient.connection.recv(1024)
        message = ''
        count = count + 1
        for i in range(53):
            decision = random.random() < 0.98
            message = message + str(int(decision))

        print count, message
        sendClient.connection.send(message)
