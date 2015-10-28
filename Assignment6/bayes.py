import getopt, sys, operator, itertools
###############################################
#                                             #
#  WARNING: This code is very gross...sorry!  #
#                                             #
###############################################

class Node():
    def __init__(self,letter,pt=None,pf=None):
        self.pt = pt
        self.pf = pf
        self.parents = None
        self.children = None
        self.conditional = {}
        self.letter = letter

def convertToArray(string):
    array = []
    isTilda = False
    for s in string:
        if s is not '~' and not isTilda:
            array.append(s)
        elif s is '~':
            isTilda = True
        elif isTilda:
            array.append('~' + s)
            isTilda = False
    return array

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

    def calcConditionalExtended(self,a,b):
        node_a = self.graph[a]
        b_list = convertToArray(b)
        b_start = b
        b = b_list[0]
        c = b_list[1]
        node_b = self.graph[b]
        node_c = self.graph[c]

        """
        if node_a.letter == node_b.letter:
            return 1
        if node_a.letter == node_c.letter:
            return 1
        """
        
        # Handle all c|ps cases given
        if node_a.letter == 'c':
            if node_b.letter == 's' and node_c.letter == 'p':
                if '~' in b: # not s
                    if '~' in c: # not p
                        if '~' in a:
                            #return node_a.conditional['~p~s']
                            return 1-node_a.conditional['~p~s']
                        else:
                            return node_a.conditional['~p~s']
                    else: # p 
                        if '~' in a:
                            #return node_a.conditional['p~s']
                            return 1-node_a.conditional['p~s']
                        else:
                            return node_a.conditional['p~s']
                else: # s
                    if '~' in c: # not p
                        if '~' in a:
                            #return node_a.conditional['~ps']
                            return 1-node_a.conditional['~ps']
                        else:
                            return node_a.conditional['~ps']
                    else: # p
                        if '~' in a:
                            #return node_a.conditional['ps']
                            return 1-node_a.conditional['ps']
                        else:
                            return node_a.conditional['ps']

            if node_c.letter == 's' and node_b.letter == 'p':
                if '~' in b: # not p
                    if '~' in c: # not s
                        if '~' in a:
                            #return node_a.conditional['~p~s']
                            return 1-node_a.conditional['~p~s']
                        else:
                            return node_a.conditional['~p~s']
                    else: # s
                        if '~' in a:
                            #return node_a.conditional['~ps']
                            return 1-node_a.conditional['~ps']
                        else:
                            return node_a.conditional['~ps']
                else: # p
                    if '~' in c: # not s
                        if '~' in a:
                            #return node_a.conditional['p~s']
                            return 1-node_a.conditional['p~s']
                        else:
                            return node_a.conditional['p~s']
                    else: # s
                        if '~' in a:
                            #return node_a.conditional['ps']
                            return 1-node_a.conditional['ps']
                        else:
                            return node_a.conditional['ps']
        
        #print a+b_start
        #print b_start
        #print ""

        # Handle every other case
        return self.calcJoint(a+b_start)/self.calcJoint(b_start)

    def calcConditional(self,a,b):
        if len(b.replace('~','')) > 1:
            return self.calcConditionalExtended(a,b)
        node_a = self.graph[a]
        node_b = self.graph[b]
        if node_a.letter == node_b.letter:
            return 1

        if node_a.parents == None and node_b.parents == None: # two top nodes
            if '~' in a:
                return node_a.pf
            else:
                return node_a.pt

        elif node_a.letter == 'c' or node_b.letter == 'c': # nodes include c
            if node_a.parents == None: # node_a is a top node
                return self.calcConditional(b,a) * self.calcMarginal(a) / self.calcMarginal(b) # bayes
            elif node_b.parents == None: # node_b is a top node
                if node_b.letter == 's' and '~' in b:
                    if '~' in a:
                        prob = (1-node_a.conditional['p~s'])*self.calcMarginal('p') + (1-node_a.conditional['~p~s'])*self.calcMarginal('~p')
                    else:
                        prob = node_a.conditional['p~s']*self.calcMarginal('p') + node_a.conditional['~p~s']*self.calcMarginal('~p')
                    return prob
                if node_b.letter == 's' and '~' not in b:
                    if '~' in a:
                        prob = (1-node_a.conditional['ps'])*self.calcMarginal('p') + (1-node_a.conditional['~ps'])*self.calcMarginal('~p')
                    else:
                        prob = node_a.conditional['ps']*self.calcMarginal('p') + node_a.conditional['~ps']*self.calcMarginal('~p')
                    return prob
                if node_b.letter == 'p' and '~' in b:
                    if '~' in a:
                        prob = (1-node_a.conditional['~ps'])*self.calcMarginal('s') + (1-node_a.conditional['~p~s'])*self.calcMarginal('~s')
                    else:
                        prob = node_a.conditional['~ps']*self.calcMarginal('s') + node_a.conditional['~p~s']*self.calcMarginal('~s')
                    return prob
                if node_b.letter == 'p' and '~' not in b:
                    if '~' in a:
                        prob = (1-node_a.conditional['ps'])*self.calcMarginal('s') + (1-node_a.conditional['p~s'])*self.calcMarginal('~s')
                    else:
                        prob = node_a.conditional['ps']*self.calcMarginal('s') + node_a.conditional['p~s']*self.calcMarginal('~s')
                    return prob
            else: # node_a or node_b is a bottom node
                if node_a.letter == 'c': # node_a is c
                    if '~' in b:
                        prob = (1-node_b.conditional[a]) * self.calcMarginal(a) / self.calcMarginal(b) # bayes
                    else:
                        prob = node_b.conditional[a] * self.calcMarginal(a) / self.calcMarginal(b) # bayes
                    return prob
                else: # node_b is c
                    if '~' in a:
                        prob = 1-node_a.conditional[b]
                    else:
                        prob = node_a.conditional[b]
                    return prob
            return 0

        else: # nodes are two apart
            prob = self.calcConditional(a,'c')*self.calcConditional('c',b)+self.calcConditional(a,'~c')*self.calcConditional('~c',b)
            return prob


    def calcJoint(self,a):
        a = convertToArray(a)
        a = list(set(a))
        def jointHelper(b): # Do the actual calculation given the list
            p = 1
            #print b
            for i in b:
                if self.graph[i].parents is not None and len(self.graph[i].parents) > 0:
                    p *= self.calcConditional(i,''.join([b.letter for b in self.graph[i].parents]))
                    #print("{0} | {1} = {2}".format(i,''.join([b.letter for b in self.graph[i].parents]),self.calcConditional(i,''.join([b.letter for b in self.graph[i].parents]))))
                    #print p
                else:
                    #print i
                    p *= self.calcMarginal(i)
                    #print p
            #print p
            return p

        ret = 0
        notInJoint = []
        notInJoint =  list(set([str(s).replace('~','') for s in self.graph.keys()]))
        a_clean = list(set(str(node).replace('~','') for node in a))
        for i in a_clean:
            if i in notInJoint:
                notInJoint.remove(i)

        length = len(notInJoint)

        binary_ops = {}
        binary = 00001
        node_order = []
        for x in (a + notInJoint):
            binary_ops[x] = binary
            node_order.append(x)
            binary = binary << 1
        #print binary_ops
        permutations = ["".join(seq) for seq in itertools.product("01", repeat=5)]
        #print notInJoint
        p = []
        final_bits = []
        # convert to int
        for i in range(len(permutations)):
            p.append(int(permutations[i],2))

        # find bits
        for i in range(len(p)):
            for j in a:
                p[i] = p[i] | binary_ops[j]
            final_bits.append(p[i])
        final_bits = set(final_bits)
        #print final_bits
        #print len(final_bits)

        # Make list of out bits
        #print "a:"
        #print a
        #print 'Not in joint:'
        #print notInJoint
        node_order.reverse()
        string_list = []
        final_list = [0,0,0,0,0]
        for interger in final_bits:
            string = "{0:05b}".format(interger)
            string_list = list(string)
            #print string
            for i in range(len(string)):
                if string_list[i] == '1':
                    if node_order[i] in (a+notInJoint):
                        final_list[i] = node_order[i]
                    else:
                        final_list[i] = '~' + node_order[i]
                    #final_list[i] = node_order[i]
                elif string_list[i] == '0':
                    final_list[i] = '~' + node_order[i]
            #print final_list
            ret += jointHelper(final_list)
        #print ret
        #print ""
        return ret 

def callJoint(a,net):
    a = convertToArray(a)
    a_clean = list(set(str(node).replace('~','') for node in a))
    a_clean = filter(None,a_clean)
    for i in range(len(a)):
        if a_clean[i].isupper():
            a_clean[i] = a_clean[i].lower()
            str1 = ''.join(a[:i]+[a_clean[i]]+a[i+1:])
            a_clean[i] = '~' + a_clean[i] 
            str2 = ''.join(a[:i]+[a_clean[i]]+a[i+1:])
            #print str1
            #print str2
            callJoint(str1,net)
            callJoint(str2,net)
            return
        else:
            pass
    #print a
    a = ''.join(a)
    print('Joint of {0} = {1}'.format(a,net.calcJoint(a)))
    return

def callConditional(a,b,net):
    b = convertToArray(b)
    b_clean = list(set(str(node).replace('~','') for node in b))
    b_clean = filter(None,b_clean)
    for i in range(len(b)):
        if b_clean[i].isupper():
            b_clean[i] = b_clean[i].lower()
            str1 = ''.join(b[:i]+[b_clean[i]]+b[i+1:])
            b_clean[i] = '~' + b_clean[i] 
            str2 = ''.join(b[:i]+[b_clean[i]]+b[i+1:])
            #print str1
            #print str2
            callConditional(a,str1,net)
            callConditional(a,str2,net)
            return
        else:
            pass
    #print a
    b = ''.join(b)
    if a.isupper:
        print('{0}|{1} = {2}'.format('~'+a.lower(),b,net.calcConditional('~'+a.lower(),b)))
    print('{0}|{1} = {2}'.format(a.lower(),b,net.calcConditional(a.lower(),b)))

    return

def main():
    p_print = 1
    try:
        opts, args = getopt.getopt(sys.argv[1:], "m:g:j:p:a:")
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
            if float(a[1:]) == .5:
                p_print = 2
            else:
                p_print = 0
            print net.setPrior(a[0], float(a[1:]))
        elif o in ("-m"):
            print "flag", o
            print "args", a
            print type(a)
            print net.calcMarginal(a.lower())
            if a.isupper():
                print net.calcMarginal('~'+a.lower())
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
            callConditional(a[:p],a[p+1:],net)
            #print net.calcConditional(a[:p], a[p+1:])
        elif o in ("-j"):
            print "flag", o
            print "args", a
            callJoint(a,net)

            #print net.calcJoint(convertToArray(a))
            """
            for i in range(0,len(a)):
                if a[i].isupper:
                    calcJoint(a[:i] + '~' + a[i:])
            """
        elif o in ("-a"):
            print ""
            print "Expected:"
            print ""
            if p_print == 1:
                print("    None  D=T   S=T   C=T   C&S=T D&S=T")
                print("P=F 0.100 0.102 0.100 0.249 0.156 0.102")
                print("S=T 0.300 0.307 1.000 0.825 1.000 1.000")
                print("C=T 0.011 0.025 0.032 1.000 1.000 0.067")
                print("X=T 0.208 0.217 0.222 0.900 0.900 0.247")
                print("D=T 0.304 1.000 0.311 0.650 0.650 1.000")
            if p_print == 2:
                print("    None  D=T   S=T   C=T   C&S=T D&S=T")
                print("P=F 0.100 0.102 0.100 0.201 0.156 0.102")
                print("S=T 0.500 0.508 1.000 0.917 1.000 1.000")
                print("C=T 0.174 0.037 0.032 1.000 1.000 0.067")
                print("X=T 0.212 0.226 0.311 0.900 0.900 0.247")
                print("D=T 0.306 1.000 0.222 0.650 0.650 1.000")
            print ""
            print "Got:"
            print ""
            print("    None  D=T   S=T   C=T   C&S=T D&S=T")
            print("P=F {:.3f} {:.3f} {:.3f} {:.3f} {:.3f} {:.3f}".format(net.calcMarginal('~p'),net.calcConditional('~p','d'),net.calcConditional('~p','s'),net.calcConditional('~p','c'),net.calcConditional('~p','cs'),net.calcConditional('~p','ds')))
            print("S=T {0:.3f} {1:.3f} {2:.3f} {3:.3f} {4:.3f} {5:.3f}".format(net.calcMarginal('s'),net.calcConditional('s','d'),net.calcConditional('s','s'),net.calcConditional('s','c'),net.calcConditional('s','cs'),net.calcConditional('s','ds')))
            print("C=T {0:.3f} {1:.3f} {2:.3f} {3:.3f} {4:.3f} {5:.3f}".format(net.calcMarginal('c'),net.calcConditional('c','d'),net.calcConditional('c','s'),net.calcConditional('c','c'),net.calcConditional('c','cs'),net.calcConditional('c','ds')))
            print("X=T {0:.3f} {1:.3f} {2:.3f} {3:.3f} {4:.3f} {5:.3f}".format(net.calcMarginal('x'),net.calcConditional('x','d'),net.calcConditional('x','s'),net.calcConditional('x','c'),net.calcConditional('x','cs'),net.calcConditional('x','ds')))
            print("D=T {0:.3f} {1:.3f} {2:.3f} {3:.3f} {4:.3f} {5:.3f}".format(net.calcMarginal('d'),net.calcConditional('d','d'),net.calcConditional('d','s'),net.calcConditional('d','c'),net.calcConditional('d','cs'),net.calcConditional('d','ds')))
            print ""
        else:
            assert False, "unhandled option"
            # ...

if __name__ == "__main__":
    main()
