import re

# Single Square brackets (excludes double brackets)
SSQR_RE = r'(?<=[^\[])\[[^\[].*?\](?=[^\]])'
# Double Square brackets
DSQR_RE = r'\[\[.*?\]\]'
# Single Angle brackets
SANG_RE = r'(?<=[^\<])\<[^\<].*?\>(?=[^\>])'
# Double Angle brackets
DANG_RE = r'\<\<.*?\>\>'

def parse_raw(txt):
    parsed = re.sub(DSQR_RE, "", txt)
    parsed = re.sub(SSQR_RE, "", parsed)
    parsed = re.sub(SANG_RE, "", parsed)
    parsed = re.sub(DANG_RE, "", parsed)
    parsed = re.sub('\n\n+', '\n', parsed)
    parsed = re.sub("\n(\w)", r" \1", parsed)
    return parsed