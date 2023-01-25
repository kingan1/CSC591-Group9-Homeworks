from row import Row
from cols import Cols
import utils
class Data :
   def __init__(self, src, x) -> None:
       self.rows = []
       self.cols = None
       if type(src) == str:
            utils.csv(src,self.add(x))
       else:
            map(self.add(x), src or []) 


   def add(self,t):
       if self.cols :
           t = t.cells and t or Row(t)
           self.rows.append(t)
           self.cols.add(t)
       else:
           self.cols = Cols(t)


   def clone(self,init,x):
        data = Data({self.cols.names})
        map(data.add(x),init or [])
        return data

   def stats(self, what,cols,nplaces):
        def fun(k,col):
            return None
        return map(fun,cols or self.cols.y)



