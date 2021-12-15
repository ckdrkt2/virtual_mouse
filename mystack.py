import numpy as np

class mystack():

    def __init__(self, max_length):
        self.max_length = max_length
        self.stack = []
        self.length = 0

    def add(self, n):
        self.stack.append(n)
        self.length += 1
        if self.length > self.max_length:
            self.stack.pop(0)
            self.length -= 1
    
    def var(self):
        if self.length == self.max_length:
            return np.var(self.stack)
        else:
            return 0

    def avg(self):
        if self.length > 0:
            return sum(self.stack)/self.length
        else:
            return 0

    def diff(self):
        if self.length == self.max_length:
            diff1 = np.diff(self.stack)
            diff2 = np.diff(diff1)
            return np.sum(diff2)
        else:
            return False

    def clear(self):
        self.stack = []
        self.length = 0