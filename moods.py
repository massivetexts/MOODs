import re
import os
import spacy
import gzip
import numpy as np
from scipy.stats import entropy
from numpy.linalg import norm

nlp = spacy.load("en_core_web_sm")

# Single Square brackets (excludes double brackets)
SSQR_RE = r'(?<=[^\[])\[[^\[].*?\](?=[^\]])'
# Double Square brackets
DSQR_RE = r'\[\[.*?\]\]'
# Single Angle brackets
SANG_RE = r'(?<=[^\<])\<[^\<].*?\>(?=[^\>])'
# Double Angle brackets
DANG_RE = r'\<\<.*?\>\>'

def JSD(P, Q, dist=False):
    ''' Jenson-Shannon Divergence - a symmetrical update to KL Divergence.
    
    dist=True returns JS distance.'''
    _P = P / norm(P, ord=1)
    _Q = Q / norm(Q, ord=1)
    _M = 0.5 * (_P + _Q)
    jsdivergence = 0.5 * (entropy(_P, _M) + entropy(_Q, _M))
    if dist:
        return np.sqrt(jsdivergence)
    else:
        return jsdivergence

def parse_raw(txt):
    # Strip Bracketed Junk
    parsed = re.sub(DSQR_RE, "", txt)
    parsed = re.sub(SSQR_RE, "", parsed)
    parsed = re.sub(SANG_RE, "", parsed)
    parsed = re.sub(DANG_RE, "", parsed)
    parsed = re.sub('\n\n+', '\n', parsed)
    parsed = re.sub("\n(\w)", r" \1", parsed)
    
    # Replace line breaks
    parsed = re.sub('\n\s+?([\w`\'])', r' \1', parsed)
    parsed = re.sub('  +', ' ', parsed)

    return parsed

def clean_words(doc, pos=['VERB', 'NOUN', 'PROPN', 'ADJ', 'ADV']):
    l = []
    for word in doc:
        if not word.is_stop and (word.pos_ in pos):
            l.append(word.lemma_.lower())
    return l

def cleaned_bow_iter(fname, dictionary, include_name=True, min_tokens_per_doc=0):
    ''' Return key, bag-of-words list from a preprocessed file (see preprocess-bills.ipynb for preprocessing code)'''
    with gzip.open(fname, mode='r') as f:
        for line in f.readlines():
            name, text = line.decode('utf-8').strip('\n').split('\t')
            bow = dictionary.doc2bow(text.split(' '))
            if include_name:
                yield name, bow
            else:
                yield bow
            
def cleaned_txts_iter(fname):
    ''' Return key, [list,of,words] list from a preprocessed file'''
    with gzip.open(fname, mode='r') as f:
        for line in f.readlines():
            name, text = line.decode('utf-8').strip('\n').split('\t')
            yield name, text.split(' ')

class Bill():
    
    def __init__(self, path):
        
        # Parse metadata from filename
        fname = os.path.split(path)[-1]
        self.name = os.path.splitext(fname)[0]

        self.congress, sponsor, self.num = self.name.split('_')
        self.sponsor = sponsor.replace('-', '.')
        
        with open(path) as f:
            self._raw = f.read()
      
    def text(self):
        txt = parse_raw(self._raw).strip()
        return txt
            
    def lines(self, nlp_doc=False):
        ''' A simplistic way of splitting up the text by newline.
        If nlp=True, returns a Spacy document rather than raw text
        '''
        lines = self.text().split('\n')
        
        for line in lines:
            # If starts with open paren (e.g. "(a)"), strip it
            if re.match('^\s*\(',line):
                line = re.sub('^.*\) *', '', line)

            # Strip hyphens, for now
            line = re.sub('--', ' ', line)
            
            if nlp_doc:
                yield nlp(line)
            else:
                yield line

    def __repr__(self):
        return "%s%s (%s congress)" % (self.sponsor, self.num, self.congress)
    
        