import math
import datetime
import copy
# from stack import Stack, Buffer

DECREASE_KEY = 0
DELETE = 1

class BufferHeap:
    def __init__(self, arr=[]):
        self.sb = []
        self.su = []
        self.r = 1 + math.floor(math.log(len(arr), 2))

        arr = sorted(arr, key=lambda x: (x.key, x.id))
        for i in range(self.r):
            bi = arr[2 ** i - 1 : 2 ** (i+1) - 1]
            ui = []
            self.sb.append(bi)
            self.su.append(ui)

    def delete_min(self):
        i = -1
        b_ = []
        while i < self.r-1 and len(b_) == 0:
            i += 1
            b_ = self.apply_updates(i, b_)
        if len(b_) > 0:
            node = self.redistribute_element(i, b_)
            return node

    def apply_updates(self, i, bi):
        bi = copy.deepcopy(self.sb[i])
        if len(bi) == 0 and i < self.r-1:
            self.su[i+1] += self.su[i]
            self.su[i] = []
        else:
            k = math.inf if i == self.r - 1 else max(bi, key=lambda x: x.key).key
            for op in sorted(self.su[i], key=lambda x: (x.id, x.timestamp)):
                if op.type == DELETE:
                    target = Node(op.id)
                    if target in bi:
                        bi.remove(target)
                elif op.type == DECREASE_KEY:
                    target = Node(op.id)
                    if target in bi:
                        original = bi[bi.index(target)]
                        original.key = min(original.key, op.value)
                    elif op.value <= k:
                        bi.append(Node(op.id, op.value))
                if i < self.r-1:
                    if op.type == DECREASE_KEY and op.value > k:
                        self.su[i+1].append(op)
                    else:
                        self.su[i+1].append(Operation(type=DELETE, id=op.id))
        self.su[i] = []
        return bi

    def split(self, b_, n):
        b_ = sorted(b_, key=lambda x: (x.key, x.id))
        return b_[: n], b_[n: ]

    def redistribute_element(self, i, b_):
        if len(b_) > 2 ** i:
            b_, bb_ = self.split(b_, 2 ** i)
            for node in bb_:
                self.su[i+1].append(Operation(type=DECREASE_KEY, id=node.id, value=node.key))
        self.sb[i] = []
        for k in range(i-1, -1, -1):
            if len(b_) > 2 ** k:
                b_, bb_ = self.split(b_, 2**k)
                self.sb[k] = bb_
        return b_[0]


    # def reconstruct(self):

    def isEmpty(self):
        return len(list(filter(lambda b: len(b) > 0, self.sb))) == 0


    def decrease_key(self, id, value):
        self.su[0].append(Operation(type=DECREASE_KEY, id=id, value=value))


class Node:
    def __init__(self, id=None, key=None):
        self.id = id
        self.key = key

    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return other.__lt__(self)

    def __eq__(self, other):
        return self.id == other.id

class Operation:
    def __init__(self, type = None, id = None, value = None):
        self.type = type
        self.id = id
        self.value = value
        self.timestamp = datetime.datetime.now()

    def __lt__(self, other):
        if self.id == other.id:
            return self.timestamp < other.timestamp
        return self.id < other.id

    def __gt__(self, other):
        return other.__lt__(self)
