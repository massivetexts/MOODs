import re
import os
import spacy
nlp = spacy.load("en_core_web_sm")

# Single Square brackets (excludes double brackets)
SSQR_RE = r'(?<=[^\[])\[[^\[].*?\](?=[^\]])'
# Double Square brackets
DSQR_RE = r'\[\[.*?\]\]'
# Single Angle brackets
SANG_RE = r'(?<=[^\<])\<[^\<].*?\>(?=[^\>])'
# Double Angle brackets
DANG_RE = r'\<\<.*?\>\>'

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



class Bill():
    
    def __init__(self, path):
        
        # Parse metadata from filename
        fname = os.path.split(path)[-1]
        name = os.path.splitext(fname)[0]

        self.congress, sponsor, self.num = name.split('_')
        self.sponsor = sponsor.replace('-', '.')
        
        with open(path) as f:
            self._raw = f.read()
      
    def text(self):
        txt = parse_raw(self._raw)
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
    
        