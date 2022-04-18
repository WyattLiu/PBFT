#!/usr/bin/python3

import socket
import random
import time
import sys
import requests
from type.GCounter import PNCounter
from type.RCounter import RCounter
from type.ORSet import ORSet
from type.Graph import Graph
from type.RGraph import RGraph
from type.Performance import Performance
from type.helper import res_parse
from type.Type import Type
from type.Action import Action
from requests.adapters import HTTPAdapter, Retry

class Server:

    def __init__(self, ip, port):
        self.num_timeout = 0
        self.ip = ip
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.s.settimeout(1)
        self.s.bind(('', 0))
        self.s.listen()
        self.cb_hostname = socket.gethostname()
        self.cb_port = port = self.s.getsockname()[1]
        self.debug_print("Callback is: " + str(self.cb_hostname) + ":" + str(self.cb_port))
        self.session = requests.Session()
        retries = Retry(total=5,
                backoff_factor=0.1,
                status_forcelist=[ 500, 502, 503, 504 ])
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
    def debug_print(self, str):
        if(0):
            print(str)
    def connect(self):
        self.debug_print("TODO:post")
    def post(self, bft_addr, string_to_send, step):
        try :
            r = self.session.post("http://"+bft_addr+"/createblock", headers={"Content-Type" : "application/json"}, data = string_to_send, timeout = 1)
            self.debug_print(str(r))
        except requests.exceptions.Timeout:
            self.debug_print("timeout POST: " + str(step))
            if(step < 5):
                self.post(bft_addr,string_to_send, step + 1)
    def pbft_send(self, text):
        self.debug_print("Forwarding to BFT: " + str(text) + " located at: " + str(self.ip) + ":" + str(self.port))
        self.debug_print("Tell pbft my hostname: " + str(self.cb_hostname) + " port: " + str(self.cb_port))
        self.debug_print("Showing pbft my intension is for " + str(self.ip))
        text = str(self.ip) + " " + str(self.cb_hostname) + " " + str(self.cb_port) + " " + text
        string_to_send = '{"timestamp": "2001-01-01 06:00:00", "carPlate": "<plate>", "block": {"data": "' + text + '"}}'
        #string_to_send = '{"carPlate": "<plate>", "block": {"data": "' + text + '"}}'
        
        self.debug_print("Raw json forwarded " + string_to_send)
        bft_addr = str(self.ip) + ":" + str(self.port)
        self.debug_print("Before Post")
        self.post(bft_addr, string_to_send, 0)
        self.debug_print("Before accept")
        conn, addr = self.s.accept()
        self.debug_print("Before recv")
        binary_data = conn.recv(1024)
        self.debug_print("Before decode")
        text = binary_data.decode("utf-8")
        self.debug_print("Before close")
        conn.close()
        self.debug_print("answer: " + text)
        return text
    def convert_back_plain_string(self, data):
        raw_string = data.decode('utf-8')
        self.debug_print("Debug:" + raw_string)
        raw_list = raw_string.splitlines()
        res = ""
        for i in raw_list:
            test = i.split(':');
            if(len(test) == 2):
                self.debug_print("i:" + i)
                res += test[1] + " "
        return res.strip()
    def send(self, data: bytes):        
        #time.sleep(1)
        return self.pbft_send(self.convert_back_plain_string(data))
        
    def disconnect(self):
        self.debug_print("Do nothing on disconnect")
        self.s.close()

def isHelp(args):
    return len(sys.argv) == 2 and (args[1] == '--help' or args[1] == '-h')

def helpMessage():
    string = ("  Go to ../RAC and follow the instruction to boot up replication server  \n\n" +
        "  [For Example] python -m http.server 8080 --bind 127.0.0.1 \n\n" +
        "  and in this folder, run: \n\n" +
        "  python client.py 127.0.0.1:<port number> \n\n" + 
        "  [For Example] python client.py 127.0.0.1:<port number> \n")
    print(string)

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

        s = Server(host, port)   

        if s.connect() == 0:
            print("connection failed")
            exit(1)

        while (True):
            text = input("Enter:").split(" ")

            typecode = text[0]

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
                print("Type \'{}\' is not valid".format(typecode))
                continue

            print(typeClass.operate(text))
    
        s.disconnect()


    




        


   
