import math
class SYM :
    """
	Summarizes a stream of Symbols.
	"""
    def __init__(self):
        self.n = 0
        self.has = {}
        self.most = 0
        self.mode = None

    """ update counts of things seen so far"""
    def add(self, x:str):
        if x != "?":
            self.n = self.n + 1 
            self.has[x] = 1 + (self.has[x] or 0)
            if self.has[x] > self.most :
                self.most = self.has[x]
                self.mode = x
   
    """ return the mode """
    def mid(self, x:str):
        return self.mode

    """return the entropy"""
    def div(self,x:str):
        def fun(p):
            return math.log(p,2)
        e=0
        for _,n in self.has.items():
            e = e + fun(n/self.n)

        return -e 
