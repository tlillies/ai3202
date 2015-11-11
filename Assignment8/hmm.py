from string import ascii_lowercase

class HMM:
    def __init__(self,input_file):
        self.input_file = input_file
        self.emission = {}
        self.transition = {}
        self.table = {}

        # create a dictionary of dictionaries
        for c in ascii_lowercase:
            self.emission[c] = {}
            self.transition[c] = {}
            self.table[c] = {}

        self.emission['_'] = {}
        self.transition['_'] = {}
        self.table['_'] = {}

        for key in self.emission:
            for c in ascii_lowercase:
                self.emission[key][c] = 0
                self.transition[key][c] = 0
                self.table[key][c] = {}
            self.emission[key]['_'] = 0
            self.transition[key]['_'] = 0
            self.table[key]['_'] = {}

        # fill with input file
        f = open(input_file)
        for line in f:
            self.emission[line[0]][line[2]] += 1
            try:
                self.transition[line[0]][(line+1)[0]] += 1
            except:
                pass

        for key in self.table:
            e_size = 0.0
            t_size = 0.0
            for key2 in self.table[key]:
                e_size += self.emission[key][key2]
                t_size += self.transition[key][key2]

            for key2 in self.table[key]:
                self.table[key][key2]['emission'] = (self.emission[key][key2]+1)/(e_size+27)
                self.table[key][key2]['transition'] =  (self.transition[key][key2]+1)/(t_size+27)


    def printHMM(self):
        print("EMISION:")
        for key in self.table:
            for key2 in self.table[key]:
                print("P({0}|{1}) = {2}".format(key2,key,self.table[key][key2]['emission']))
        print("###########################################")
        print("TRANSITIONAL:")
        for key in self.table:
            for key2 in self.table[key]:
                print("P({0}|{1}) = {2}".format(key2,key,self.table[key][key2]['transition']))


hmm = HMM('typos20.data')
hmm.printHMM()
