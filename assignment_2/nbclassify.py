import sys
import os
import string
import math

class NB:
    
    def __init__(self, c_path):
        
        self.base_path = c_path
        self.prior = dict()

        self.token_conditionals = dict()       #T
        self.total_tokens = dict()      #C
        self.B = 0                      #B

        self.classes = ['n', 'p', 't', 'd']
        self.token_conditionals['n'] = dict()
        self.token_conditionals['p'] = dict()
        self.token_conditionals['t'] = dict()
        self.token_conditionals['d'] = dict()

        self.files = dict()          #path: [label_1, label_2]
        self.read_parameters()
        self.get_files()
    def read_parameters(self):
        infile = open("nbmodel.txt", "r")

        for c in self.classes:
            self.prior[c] = float(infile.readline().strip())

        for line in infile:
            parts = line.split(' ')
            for i,c in enumerate(self.classes):
                self.token_conditionals[c][parts[0]] = float(parts[i+1] )
        infile.close()

    def apply_multinomial_NB(self, C,V,prior,condprob, d):
        W = self.extract_tokens_from_docs(V,d)
        score = dict()
        result = ['','']
        for c in self.classes:
            score[c] = math.log(1.0 + prior[c])
            for t in W:
                score[c] += math.log(condprob[c][t])
        if score['n'] > score['p']:
            result[1] = 'n'
        else:
            result[1] = 'p'
        if score['t'] > score['d']:
            result[0] = 't'
        else:
            result[0] = 'd'
        return result
 
    def classify(self):
        for f in self.files:
            r = self.apply_multinomial_NB(self.classes,self.token_conditionals['n'],self.prior, self.token_conditionals, f)
            if r[1] == 'n':
                self.files[f][1] = "negative"
            else:
                self.files[f][1] = "positive"
            if r[0] == 't':
                self.files[f][0] = "truthful"
            else:
                self.files[f][0] = "deceptive"

    def extract_tokens_from_docs(self, V,d):
        W = list()
        infile = open(d, "r")
        s = infile.read().split(' ')
        for word in s:
            word = word.strip().translate(string.maketrans("",""), string.punctuation).lower()
            if not word.isalnum():
                continue
            if word in V:
                W.append(word)
        infile.close()
        return W

    def get_files(self):
        l1_folders = os.listdir(self.base_path)
        for folder in l1_folders:
            if folder == ".DS_Store":
                continue
            f2_path = self.base_path +"/" + folder
            if not os.path.isdir(f2_path):
                continue
            l2_folders = os.listdir(f2_path)
            for f2 in l2_folders:
                if f2 == ".DS_Store":
                    continue
                f3_path = f2_path + "/" + f2
                l3_folders = os.listdir(f3_path)
                for f3 in l3_folders:
                    if f3 == ".DS_Store":
                        continue
                    f4_path = f3_path + "/" + f3
                    l4_folders = os.listdir(f4_path)
                    for f in l4_folders:
                        if f == ".DS_Store":
                            continue
                        file_path = f4_path + "/" + f
                        self.files[file_path] = ["", ""]
                     
            

    def write_output(self):
        outfile = open('nboutput.txt', 'w')
        for file in self.files:
            outfile.write(self.files[file][0] + " " + self.files[file][1] + " " + file+"\n")


input_path = sys.argv[1]
classifier = NB(input_path)
classifier.classify()
classifier.write_output()
