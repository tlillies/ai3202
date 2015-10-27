import getopt, sys
class Node():
    def __init__(self,letter,pt=None,pf=None):
        self.pt = pt
        self.pf = pf
        self.parents = None
        self.children = None
        self.conditional = {}
        self.letter = letter

def makeGraph():
    graph = {}
    P = Node('p',.9,.1)
    S = Node('s',.3,.7)
    X = Node('x')
    C = Node('c')
    D = Node('d')

    P.children = [C]
    S.children = [C]
    C.parents = [P,S]
    C.children = [D,X]
    X.parents = [C]
    D.parents = [C]

    C.conditional['~ps'] = 0.05
    C.conditional['~p~s'] = 0.02
    C.conditional['ps'] = 0.03
    C.conditional['p~s'] = .001

    X.conditional['c'] = .9
    X.conditional['~c'] =.2

    D.conditional['c'] = .65
    D.conditional['~c'] =.30

    graph['p'] = P
    graph['~p'] = P
    graph['d'] = D
    graph['~d'] = D
    graph['c'] = C
    graph['~c'] = C
    graph['x'] = X
    graph['~x'] = X
    graph['s'] = S
    graph['~s'] = S

    return graph

class BayesNet():
    def __init__(self):
        self.graph = makeGraph() 
    def setPrior(self,node,prob):
        self.graph[node].pt = prob
        self.graph[node].pf = 1-prob
        return
    def calcMarginal(self,a):
        node = self.graph[a]
        if node != None:
            if node.parents == None: # marginal of p or s
                if '~' in a:
                    return node.pf
                else:
                    return node.pt
            elif node.children == None: # marginal of d or s
                prob = node.conditional['c']*self.calcMarginal('c')
                prob += node.conditional['~c']*self.calcMarginal('~c')
                if '~' in a:
                    return 1-prob
                else:
                    return prob
            else: # marginal of c
                prob = node.conditional['ps']*self.calcMarginal('s')*self.calcMarginal('p')
                prob += node.conditional['~ps']*self.calcMarginal('s')*self.calcMarginal('~p')
                prob += node.conditional['p~s']*self.calcMarginal('~s')*self.calcMarginal('p')
                prob += node.conditional['~p~s']*self.calcMarginal('~s')*self.calcMarginal('~p')
                if '~' in a:
                    return 1-prob
                else:
                    return prob
        else:
            print "Tried to get marginal of non-singular value"


    def calcConditional(self,a,b):
        return
    def calcJoint(self,a):
        return

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "m:g:j:p:")
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        sys.exit(2)
    net = BayesNet()
    for o, a in opts:
        if o in ("-p"):
            print "flag", o
            print "args", a
            print a[0]
            print float(a[1:])
            #setting the prior here works if the Bayes net is already built
            print net.setPrior(a[0], float(a[1:]))
        elif o in ("-m"):
            print "flag", o
            print "args", a
            print type(a)
            print net.calcMarginal(a)
        elif o in ("-g"):
            print "flag", o
            print "args", a
            print type(a)
            '''you may want to parse a here and pass the left of |
            and right of | as arguments to calcConditional
            '''
            p = a.find("|")
            print a[:p]
            print a[p+1:]
            print net.calcConditional(a[:p], a[p+1:])
        elif o in ("-j"):
            print "flag", o
            print "args", a
        else:
            assert False, "unhandled option"
            # ...

if __name__ == "__main__":
    main()
