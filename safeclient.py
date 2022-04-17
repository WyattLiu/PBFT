#!/usr/bin/python3

import socket
import random
import time
import sys
import json
from _thread import *
import threading
from type.GCounter import PNCounter
from type.RCounter import RCounter
from type.ORSet import ORSet
from type.Graph import Graph
from type.RGraph import RGraph
from type.Performance import Performance
from type.helper import res_parse
from type.Type import Type
from type.Action import Action


class Server:

    def __init__(self, ip, port):
        self.num_timeout = 0
        self.s = None
        self.ip = ip
        self.port = port

    def connect(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.connect((self.ip, self.port))
            return 1
        except Exception as e:
            print(e)
            return 0

    def response(self) -> bytes:
        try:
            self.s.settimeout(60)
            msg = self.s.recv(1024)
            self.s.settimeout(None)
        except socket.timeout:
            self.disconnect()
            if self.num_timeout < 5:
                self.connect()
                print("Timeout on receive")
                self.num_timeout += 1
            else:
                raise socket.timeout
            return "F"

        return msg

    def send(self, data: bytes):            
        self.s.send(data)
        res = self.response()
        if res != "F":
            return res_parse(res)
        else:
            return "F"


    def disconnect(self):
        self.s.close()        

def debug_print(str):
    if(0):
        print(str)

def isHelp(args):
    return len(sys.argv) == 2 and (args[1] == '--help' or args[1] == '-h')

def helpMessage():
    string = ("  Go to ../RAC and follow the instruction to boot up replication server  \n\n" +
        "  [For Example] python -m http.server 8080 --bind 127.0.0.1 \n\n" +
        "  and in this folder, run: \n\n" +
        "  python client.py 127.0.0.1:<port number> \n\n" + 
        "  [For Example] python client.py 127.0.0.1:<port number> \n")
    print(string)

def threaded(conn):
    binary_data = conn.recv(1024)
    conn.close()
    text = binary_data.decode("utf-8")
    obj = json.loads(text)
    payload = obj['data']
    debug_print("Payload " + payload)
    text = payload.split(" ")
    return_host = text[0]
    return_port = text[1]
    return_addr = text[0] + " " + text[1]
    text = text[2:]
    debug_print("Remote cmd split: " + str(text))
    typecode = text[0]
    typeClass = None
    if (typecode == Type.DISCONNECT):
        s.disconnect()
        exit(0)
        uid = text[1]
        opcode = text[2]
        typeClass = None

    if (typecode == Type.PNCOUNTER):
        typeClass = PNCounter(s)
        
    elif (typecode == Type.RCOUNTER):
        typeClass = RCounter(s)
                        
    elif (typecode == Type.ORSET):
        typeClass = ORSet(s)
        
    elif (typecode == Type.RGRAPH):
        typeClass = RGraph(s)
                    
    elif (typecode == Type.PERFORMANCE):
        typeClass = Performance(s)
        
    else:
        result = str("Type \'{}\' is not valid".format(typecode))
    
    if(1):
        debug_print("Operating with cmd: " + str(text))
        if(typeClass != None):
            result = typeClass.operate(text)
        debug_print("Result: " + result)
        result = return_addr + " " + result
        debug_print("Forward back " + result)
        #conn.sendall(result.encode('utf-8'))
        #conn.close()
        bfts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bfts.connect((return_host, int(return_port)))
        bfts.send(result.encode('utf-8'))
        bfts.close()


if __name__ == "__main__":
    if isHelp(sys.argv):
        helpMessage()

    else:
        if len(sys.argv) < 2:
            raise ValueError('wrong arg')
    
        # gc <key> <action> [value]
        address = sys.argv[1]
        host = address.split(":")[0]
        port = int(address.split(":")[1])
        debug_print("Pased addr: " + host + " port: " + str(port))
        s = Server(host, port)   
        if s.connect() == 0:
            print("connection failed")
            exit(1)
        # we are ready to forward
        # hardcode port
        port = 60003
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', port))
        sock.listen()
        print("Bind " + str(port))
        while (True):
            conn, addr = sock.accept()
            #text = input("Enter:").split(" ")
            start_new_thread(threaded, (conn,))

        s.disconnect()


    




        


   
