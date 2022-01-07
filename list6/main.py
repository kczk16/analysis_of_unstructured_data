import PyPDF2
import spacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from spacy import displacy
from collections import Counter
import itertools


pdfFileObj = open("book.pdf", 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

pageObj = pdfReader.getPage(25)
ex = pageObj.extractText()


def get_char_per_page():
    char_dict = {i: [] for i in range(750)}
    for i in range(750):
        pageObj = pdfReader.getPage(i)
        ex = pageObj.extractText()
        ne_tree = nltk.ne_chunk(pos_tag(word_tokenize(ex)))
        char_dict[i]=[j.leaves() for j in ne_tree if type(j)!=tuple and j.label()=='PERSON']
        names = []
        for l_krotek in char_dict[i]:
            name = ""
            for j in range(len(l_krotek)):
                name = name + l_krotek[j][0] + " "
            names.append(name.strip())
        char_dict[i] = names
    return char_dict

t = get_char_per_page()

accep = ['Harry',
 'Potter',
 'Mr. Crouch',
 'Voldemort',
 'Hermione',
 'Ron',
 'Mr. Weasley',
 'Fred',
 'George',
 'Sirius',
 'Dumbledore',
 'Hagrid',
 'Bagman',
 'Krum',
 'Cedric',
 'Dobby',
 'Moody',
 'Snape',
 'Karkaroff']


# for page in t.keys():
#     new_char = []
#     for char in t[page]:
#         if char in accep:
#             new_char.append(char)
#     t[page] = new_char

def filter_char(char_per_page, accepted_char):
    for page in char_per_page.keys():
        new_char = []
        [new_char.append(char) for char in char_per_page[page] if char in accepted_char]
        char_per_page[page] = new_char
    return char_per_page


def get_authors_pairs():
    char_dict = get_char_per_page()
    char_comb_list = []
    for page in char_dict.keys():
        combinations = list(itertools.combinations(char_dict[page], 2))
        print(combinations)
        for pair in combinations:
            char_comb_list.append(list(pair))
    return dict(Counter(tuple(sorted(tup)) for tup in char_comb_list))

xd = get_authors_pairs()

