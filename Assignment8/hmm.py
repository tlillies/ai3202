from string import ascii_lowercase
import math
import operator

class HMM:
    def __init__(self,input_file):
        self.input_file = input_file
        self.emission = {}
        self.transition = {}
        self.table = {}
        self.initial = {}
        self.alphabet = []

        for c in ascii_lowercase:
            self.alphabet.append(c)

        self.alphabet.sort()
        self.alphabet.append('_')

        # create a dictionary of dictionaries
        for c in self.alphabet:
            self.emission[c] = {}
            self.transition[c] = {}
            self.table[c] = {}
            self.initial[c] = 0.0

        for key in self.emission:
            for c in self.alphabet:
                self.emission[key][c] = 0.0
                self.transition[key][c] = 0.0
                self.table[key][c] = {}

        # fill with input file
        f = open(input_file)
        i_size = 0
        previous_line = None
        while True:
            line1 = f.readline() # read in two lines at a time
            line2 = f.readline()
            if not line1: break  # EOF
            if previous_line:
                self.transition[previous_line[0]][line1[0]] += 1.0
            self.initial[line1[0]] += 1.0
            self.emission[line1[0]][line1[2]] += 1.0
            i_size += 1.0

            if not line2: break  # EOF
            self.emission[line2[0]][line2[2]] += 1.0
            self.initial[line2[0]] += 1.0
            self.transition[line1[0]][line2[0]] += 1.0
            previous_line = line2
            i_size += 1.0

        # calculate probablities
        for key in self.table:
            e_size = 0.0
            t_size = 0.0

            for key2 in self.table[key]:
                e_size += self.emission[key][key2]
                t_size += self.transition[key][key2]

            for key2 in self.table[key]:
                self.table[key][key2]['emission'] = (self.emission[key][key2]+1)/(e_size+27)
                self.table[key][key2]['transition'] =  (self.transition[key][key2]+1)/(t_size+27)

            self.initial[key] = self.initial[key]/i_size


    def printHMM(self):
        print("EMISION:")
        print("P(Et | Xt)")
        print("")
        for key in self.alphabet:
            for key2 in self.alphabet:
                print("P({0} | {1}) = {2}".format(key2,key,self.table[key][key2]['emission']))

        print("###########################################")
        print("TRANSITIONAL:")
        print("P(Xt+1 | Xt)")
        print("")
        for key in self.alphabet:
            for key2 in self.alphabet:
                print("P({0} | {1}) = {2}".format(key2,key,self.table[key][key2]['transition']))

        print("###########################################")
        print("MARGINAL:")
        for key in self.alphabet:
            print("P({0}) = {1}".format(key,self.initial[key]))

    def viterbi(self,input_file):
        """
        observed = []
        correct = []
        path = {}

        f = open(input_file)
        for line in f:
            if line[0] in self.alphabet:
                correct.append(line[0])
                observed.append(line[2])

        f.close()

        memo = [{} for i in xrange(len(observed))]

        for state in self.alphabet:
            path[state] = [state]
            memo[0][state] = math.log(self.initial[state]) + math.log(self.table[observed[0]][state]['emission'])


        for i in xrange(1,len(observed)):
            nuPath = {}

            for state in self.alphabet:
                (prob, st)  = max((memo[i-1][e] + math.log(self.table[e][state]['transition']) + math.log(self.table[state][observed[i]]['emission']),e) for e in self.alphabet)
                memo[i][state] = prob
                nuPath[state] = path[st] + [state]

            path = nuPath
        n = len(observed) - 1
        (prob, state) = max((memo[n][y], y) for y in self.alphabet)
        differencesnum = 0.0
        for x,y in zip(path[state],correct):
            if x is y:
                pass
            else:
                differencesnum += 1.
        print differencesnum/len(path[state])
        """
        f = open(input_file)
        outputs = []
        states_list = []
        vitierbi = []

        path = {}

        for line in f:
            if line[0] in self.alphabet:
                states_list.append(line[0])
                outputs.append(line[2])

        solution = []
        max_sol = []
        for x in range(len(states_list)):
            states = {}
            states_2 = {}
            for c in self.alphabet:
                states[c] = {}
            solution.append(states)
            max_sol.append(states_2)


        stateNum = 0
        firstState = True
        for observed in outputs:
            if firstState == True:
                for state in self.alphabet:
                    max_sol[stateNum][state] = math.log(self.table[state][observed]['emission']) + math.log(self.initial[state])
                    path[state] = [state]
                firstState = False
            else:
                new_path = {}
                for state in self.alphabet:
                    for previousState in self.alphabet:
                        #print max_sol[stateNum-1][previousState]
                        solution[stateNum][state][previousState] = math.log(self.table[state][observed]['emission']) +\
                                math.log(self.table[previousState][state]['transition']) +\
                                max_sol[stateNum-1][previousState]
                        (st,prob) = max(solution[stateNum][state].iteritems(), key=operator.itemgetter(1))
                    max_sol[stateNum][state] = prob
                    new_path[state] = path[st] + [state]
                path = new_path
            stateNum += 1

        (p,s) = max((max_sol[len(outputs)-1][y],y) for  y in self.alphabet)
        viterbi = path[s]
        count = 0.0
        for i in range(len(outputs)):
            if outputs[i] != states_list[i]:
                count += 1

        print("State Sequence:")
        for i in range(len(viterbi)):
            print(viterbi[i])

        print("Before Viterbi {0}% error".format(count/len(outputs)*100))
        count = 0.0
        for i in range(len(viterbi)):
            if viterbi[i] != states_list[i]:
                count += 1
        print("After Viterbi {0}% error".format(count/len(viterbi)*100))

        
hmm = HMM('typos20.data')
hmm.viterbi('typos20Test.data')
#hmm.printHMM()
