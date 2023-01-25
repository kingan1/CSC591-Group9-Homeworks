from row import Row
from cols import Cols
import utils
class Data :
   def __init__(self, src) -> None:
       self.rows = []
       self.cols = None
       if type(src) == str:
            utils.csv(src,self.add)
       else:
        map(self.add(self), src or []) 


   def add(self,t):
       if self.cols :
           t = (t.cells and t) or Row(t)
           t.append(self.rows)
           self.cols.add(t)
       else:
           self.cols = Cols(t)


   def clone(self,init):
        data = Data([self.cols.names])
        map(self.add(data),init or [])
        return data

   def stats(self, what,cols,nplaces):
        def fun(k,col):
            return None
        return map(fun,cols or self.cols)



