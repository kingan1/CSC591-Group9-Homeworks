from utils import dist, many, any

def half(data, rows = None, cols = None, above = None):
        def gap(r1, r2):
            return dist(data, r1, r2, cols)
        def cos(a, b, c):
            return (a**2 + c**2 - b**2)/(2*c)
        def proj(r):
            return {'row': r, 'x': cos(gap(r, A), gap(r, B), c)}
        rows = rows or data.rows
        some = many(rows,512)
        A = above if above else any(some)
        tmp = sorted([{"row": r, "d": gap(r, A)} for r in some], key=lambda x: x["d"])
        far = tmp[int(len(tmp)* 0.95)]
        B, c = far["row"], far["d"]
        sorted_rows = sorted(map(proj, rows), key=lambda x: x["x"])
        left, right = [], []
        for n, two in enumerate(sorted_rows):
            if n <= (len(rows) - 1) / 2:
                left.append(two["row"])
            else:
                right.append(two["row"])
        return left, right, A, B, c
    
def tree(data, rows = None, cols = None, above = None):
    rows = rows if rows else data.rows

    here = {"data" : data.clone(data, rows)}

    if len(rows)>=2*(len(data.rows)** 0.5):

        left, right, A, B, _ = half(data, rows, cols, above)
        here["left"] = tree(data, left, cols, A)
        here["right"] = tree(data, right, cols, B)

    return here

def showTree(tree, lvl=0):
    if tree:
        print("{}[{}] ".format(("|.. ")*lvl, len(tree['data'].rows)), end="")
        print((lvl==0 or not tree.get('left', None)) and (tree['data'].stats()) or "")
        showTree(tree.get('left',None), lvl+1)
        showTree(tree.get('right',None),lvl+1)