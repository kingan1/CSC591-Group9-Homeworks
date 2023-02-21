

def showTree(tree, lvl=0):
    if tree:
        print("{}[{}] ".format(("|.. ") * lvl, len(tree['data'].rows)), end="")
        print((lvl == 0 or not tree.get('left', None)) and (tree['data'].stats()) or "")
        showTree(tree.get('left', None), lvl + 1)
        showTree(tree.get('right', None), lvl + 1)
