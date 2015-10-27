import getopt, sys
class Node():
    def __init__(self,letter,pt=None,pf=None):
        self.Pt = pt
        self.Pf = pf
        self.parent = None
        self.children = None
        self.conditional = {}
        self.letter = letter

def makeGraph():
    graph = {}
    P = Node('p',.9,.1)
    D = Node('d',.3,.7)
    X = Node('x')
    C = Node('c')
    S = Node('s')

    P.Children = [C]
    S.Children = [C]
    C.Parents = [P,S]
    C.Children = [D,X]
    X.Parents = [C]
    D.Parents = [C]

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

class BayesNet():
    def __init__(self):
        self.graph = makeGraph() 
    def setPrior(self,node,prob):
        self.graph[node].pt = prob
        self.graph[node].pf = 1-prob
        return
    def calcMarginal(self,a):
        node = graph[a]
        if node != None:
            if node.Parent == None: # marginal of p or s
                if '~' in a:
                    return node.pf
                else:
                    return node.pt
            elif node.Children == None: # marginal of d or s
                prob = node.Conditional['c']*calcMarginal('c')
                prob += node.Conditional['~c']*calcMarginal('~c')
                if '~' in a:
                    return 1-prob
                else:
                    return prob
            else: # marginal of c
                prob = node.Conditional['sp']*calcMarginal('s')*calcMarginal('p')
                prob += node.Conditional['s~p']*calcMarginal('s')*calcMarginal('~p')
                prob += node.Conditional['~sp']*calcMarginal('~s')*calcMarginal('p')
                prob += node.Conditional['~s~p']*calcMarginal('~s')*calcMarginal('~p')
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
            net.setPrior(a[0], float(a[1:])
        elif o in ("-m"):
            print "flag", o
            print "args", a
            print type(a)
            net.calcMarginal(a)
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
            net.calcConditional(a[:p], a[p+1:])
        elif o in ("-j"):
            print "flag", o
            print "args", a
        else:
            assert False, "unhandled option"
            # ...

if __name__ == "__main__":
    main()
