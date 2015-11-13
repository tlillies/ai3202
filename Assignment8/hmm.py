from string import ascii_lowercase

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
                print("P({0} | {1}) = {2:.6f}".format(key2,key,self.table[key][key2]['emission']))

        print("###########################################")
        print("TRANSITIONAL:")
        print("P(Xt+1 | Xt)")
        print("")
        for key in self.alphabet:
            for key2 in self.alphabet:
                print("P({0} | {1}) = {2:.6f}".format(key2,key,self.table[key][key2]['transition']))

        print("###########################################")
        print("MARGINAL:")
        for key in self.alphabet:
            print("P({0}) = {1:.6f}".format(key,self.initial[key]))


hmm = HMM('typos20.data')
hmm.printHMM()
