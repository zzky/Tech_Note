#!/usr/bin/python3
import numpy as np
from sklearn.decomposition import PCA
from typing import List

class Word:
    def __init__(self, text, vector):
        self.text = text
        self.vector = vector

    def __str__(self):
        return self.text + ' : ' + str(self.vector)

    def __repr__(self):
        return self.__str__()



class Sentence:
    def __init__(self, word_list):
        self.word_list = word_list


    def len(self) -> int:
        return len(self.word_list)

    def __str__(self):
        word_str_list = [word.text for word in self.word_list]
        return ' '.join(word_str_list)

    def __repr__(self):
        return self.__str__()



def get_word_frequency(word_text):
    return 0.0001 


def sentence_to_vec(sentence_list: List[Sentence], embedding_size: int, a: float=1e-3):
    sentence_set = []
    for sentence in sentence_list:
        vs = np.zeros(embedding_size) 
        sentence_length = sentence.len()
        for word in sentence.word_list:
            a_value = a / (a + get_word_frequency(word.text)) 
            vs = np.add(vs, np.multiply(a_value, word.vector)) 

        vs = np.divide(vs, sentence_length) 
        sentence_set.append(vs) 

 
    pca = PCA()
    pca.fit(np.array(sentence_set))
    u = pca.components_[0] 
    u = np.multiply(u, np.transpose(u))  

   
    if len(u) < embedding_size:
        for i in range(embedding_size - len(u)):
            u = np.append(u, 0) 

    sentence_vecs = []
    for vs in sentence_set:
        sub = np.multiply(u,vs)
        sentence_vecs.append(np.subtract(vs, sub))

    return sentence_vecs
