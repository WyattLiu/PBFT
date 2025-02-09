from .helper import msg_construct
from .helper import req_construct
from type.Action import Action

class ORSet:

    def __init__(self, s):
        self.server = s

    def get(self, id):
        req = req_construct("os", id, "g", [])
        req = msg_construct(self.server, req)

        res = self.server.send(req)
        return res

    def set(self, id):
        req = req_construct("os", id, "s", [])
        req = msg_construct(self.server, req)
        
        res = self.server.send(req)
        return res

    def add(self, id, value):
        req = req_construct("os", id, "a", [str(value)])
        req = msg_construct(self.server, req)

        res = self.server.send(req)
        return res

    def remvoe(self, id, value):
        req = req_construct("os", id, "rm", [str(value)])
        req = msg_construct(self.server, req)

        res = self.server.send(req)
        return res


    def operate(self, text):

        uid = text[1]
        opcode = text[2]
        output = ''
        if (opcode == Action.GET):
            output = str((self.get(uid)))
        elif (opcode == Action.SET):
            output = str((self.set(uid)))
        elif (opcode == Action.ADD):
            value = text[3]
            output = str((self.add(uid, value)))
        elif (opcode == Action.REMOVE):
            value = text[3]
            output = str((self.remvoe(uid, value)))
        else:
            output = str(("Operation \'{}\' is not valid".format(opcode)))
        
        return output
