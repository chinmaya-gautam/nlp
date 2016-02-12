import sys
import os
import string

class NB:
    def __init__(self, base_loc):
        self.locations = dict()
        self.prior = dict()
        self.token_count = dict()
        self.total_tokens = dict()
        self.conditionals = dict()
        self.base_loc = base_loc

        self.classes = ['n', 'p', 't', 'd']

        self.locations = {base_loc + "/negative_polarity/truthful_from_Web" : ['n','t'], 
                          base_loc + "/negative_polarity/deceptive_from_MTurk": ['n', 'd'],
                          base_loc + "/positive_polarity/truthful_from_TripAdvisor":['p','t'], 
                          base_loc + "/positive_polarity/deceptive_from_MTurk": ['p', 'd']}

        
        #training data related values
        #will be calculated and rectified later

        ''' Value of B according to the training Set '''
        self.B = 0                        # B = |V| = vocab count

        ''' Value of C for each class'''
        self.total_tokens['n'] = 0            # number of tokens in all negative truthfull reviews summed up
        self.total_tokens['p'] = 0            # same 
        self.total_tokens['t'] = 0            # for 
        self.total_tokens['d'] = 0            # the rest three classes.

        ''' Value of T for each class '''
        self.token_count['n'] = dict()   # The dictionary will contain
        self.token_count['p'] = dict()   # token count of each 
        self.token_count['t'] = dict()   # token found in the
        self.token_count['d'] = dict()   # corresponding class

        self.conditionals['n'] = dict()
        self.conditionals['p'] = dict()
        self.conditionals['t'] = dict()
        self.conditionals['d'] = dict()

    def learn(self):
        V,prior, condprob = self.train_multinomial_NB(self.classes, self.locations)
        self.write_parameters(V, condprob, prior)

    def train_multinomial_NB(self, C, D):
        V = self.extract_vocabulary(D)
        N = self.count_docs(D)
        T = dict()
        condprob = dict()
        prior = dict()

        for c in C:
            T[c] = dict()
            condprob[c] = dict()
            sTct1 = 0
            Nc = self.count_docs_in_class(D,c)
            prior[c] = float(Nc)/N 
            #textc = self.concatenate_text_of_all_docs_in_class(D, c)
            self.get_token_counts(D)

            for t in V:
                T[c][t] = self.count_tokens_from_terms(c, t)
            for t in T[c]:
                sTct1 += T[c][t] + 1
            for t in V:
                condprob[c][t] = float(T[c][t] + 1)/sTct1 ## to do
        return V, prior, condprob

    def write_parameters(self,V,condprob,prior):
        file = open("nbmodel.txt", "w")
        for c in self.classes:
            file.write(str(prior[c]) + "\n")

        for v in V:
            line = v
            for c in self.classes:
                line += " " + str(condprob[c][v])
            line += "\n"
            file.write(line)

        for c in self.classes:
            for word in self.conditionals[c]:
                file.write(word + " " + str(self.conditionals[c][word]) + "\n")
        file.close()

    def extract_vocabulary(self, D):
        V = list()
        for p in D:
            folds = os.listdir(p)
            for fold in folds:
                fold_path = p + "/" + fold
                if os.path.isdir(fold_path):
                    files = os.listdir(fold_path)
                    if '.DS_Store' in files:
                        files.remove('.DS_Store')
                    for f in files:
                        file_path = fold_path + "/" + f
                        infile = open(file_path, "r")
                        s = infile.read().split(' ')
                        for word in s:
                            word = word.strip().translate(string.maketrans("",""), string.punctuation).lower()
                            if not word.isalnum():
                                continue
                            if word not in V:
                                V.append(word)
                        infile.close()
        return V

    def count_docs(self, D):
        N = 0
        for p in D:
            folds = os.listdir(p)
            for fold in folds:
                fold_path = p + "/" + fold
                if os.path.isdir(fold_path):
                    files = os.listdir(fold_path)
                    if '.DS_Store' in files:
                        files.remove('.DS_Store')
                    N += len(files)
        return N
    def count_docs_in_class(self, D, c):
        N = 0
        for p in D:
            folds = os.listdir(p)
            for fold in folds:
                fold_path = p + "/" + fold
                if os.path.isdir(fold_path):
                    files = os.listdir(fold_path)
                    if '.DS_Store' in files:
                        files.remove('.DS_Store')
                    if c in D[p]:
                        N += len(files)
        return N
    def concatenate_text_of_all_docs_in_class(self, D, c):
        text = []
        for p in D:
            if c not in D[p]:
                continue
            folds = os.listdir(p)
            for fold in folds:
                fold_path = p + "/" + fold
                if os.path.isdir(fold_path):
                    files = os.listdir(fold_path)
                    if '.DS_Store' in files:
                        files.remove('.DS_Store')
                    for f in files:
                        file_path = fold_path + "/" + f
                        infile = open(file_path, "r")
                        s = infile.read().split(' ')
                        for word in s:
                            word = word.strip().translate(string.maketrans("",""), string.punctuation).lower()
                            if not word.isalnum():
                                continue
                            text.append(word)
        return text
    def get_token_counts(self, D):
        for c in self.classes:
            for p in D:
                if c not in D[p]:
                    continue
                folds = os.listdir(p)
                for fold in folds:
                    fold_path = p + "/" + fold
                    if os.path.isdir(fold_path):
                        files = os.listdir(fold_path)
                        if '.DS_Store' in files:
                            files.remove('.DS_Store')
                        for f in files:
                            file_path = fold_path + "/" + f
                            infile = open(file_path, "r")
                            s = infile.read().split(' ')
                            for word in s:
                                word = word.strip().translate(string.maketrans("",""), string.punctuation).lower()
                                if not word.isalnum():
                                    continue
                                if word not in self.token_count[c]:
                                    self.token_count[c][word] = 1
                                else:
                                    self.token_count[c][word]+=1

    def count_tokens_from_terms(self, c, t):
        
        if t in self.token_count[c]:
            return self.token_count[c][t]
        else:
            return 0
    
input_path = sys.argv[1]
classifier = NB(input_path)
classifier.learn()

