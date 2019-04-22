'''
structure of a sentence:
<start> command color* preposition letter* digit* adverb <end>

structure of an .align:
...
starttime endtime word
...
sil: <start>, <end>

'''

'''
an example of .align:

0 13750 sil
13750 20000 bin
20000 28000 blue
28000 33250 at
33250 37750 e
37750 51250 seven
51250 61500 soon
61500 74500 sil
'''


import numpy as np

class Align(object):
    def __init__(self, absolute_max_string_len=32, label_func=None): # label_func usually takes text_to_labels in ../helpers.py
        self.label_func = label_func
        self.absolute_max_string_len = absolute_max_string_len

    def from_file(self, path):
        with open(path, 'r') as f:
            lines = f.readlines() # return the list of all the lines in the file
        align = [(int(y[0])/1000, int(y[1])/1000, y[2]) for y in [line.strip().split(" ") for line in lines]]
        # align = [(0,13.75,sil),(13.75, 20, bin),...,(61.5,74.5,sil)]: a list of tuple
        self.build(align) #build align
        return self

    def from_array(self, align):
        self.build(align)
        return self

    def build(self, align):
        self.align = self.strip(align, ['sp','sil']) #align = [(13.75, 20, bin),...,(51.25,61.5,soon)]
        self.sentence = self.get_sentence(align) # sentence = "bin blue at e seven soon"
        self.label = self.get_label(self.sentence) # label = [1,8,13,26,1,11,20,4,26,0,19,26,4,26,18,4,21,4,13,26,18,14,14,13] using text_to_labels
        self.padded_label = self.get_padded_label(self.label) #padded_label = array([ 1.,  8.,..., 14., 13., -1., -1., -1., -1., -1., -1.])

    #for an align, extract meaningful lines, ignore lines with 'sil', 'sp'
    def strip(self, align, items):
        return [sub for sub in align if sub[2] not in items]
        # [(13.75, 20, bin),...,(51.25,61.5,soon)]
    
    # assemble the sentence from align
    def get_sentence(self, align):
        return " ".join([tup[-1] for tup in align if tup[-1] not in ['sp', 'sil']])
        # "bin blue at e seven soon"

    def get_label(self, sentence):
        return self.label_func(sentence)
    
    # padded label with -1 to keep them same length
    def get_padded_label(self, label):
        padding = np.ones((self.absolute_max_string_len-len(label))) * -1
        return np.concatenate((np.array(label), padding), axis=0) 
    # array([ 1.,  8.,..., 14., 13., -1., -1., -1., -1., -1., -1.])

    @property
    def word_length(self):
        return len(self.sentence.split(" "))

    @property
    def sentence_length(self):
        return len(self.sentence)

    @property
    def label_length(self):
        return len(self.label)
