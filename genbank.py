"""Reads the Gene databases and processes the raw data into useful information."""

def parse_DNA(filename):
    """Extracts the DNA sequence from .gbk files."""
    fp = file(filename)
    data = fp.read()
    fp.close()
    orgn = data.find('ORIGIN') #Locates the word ORIGIN in the file, which only appears once. 
    start = data.find('1', orgn) #Locates the start of the DNA Sequence, normally after 'ORIGIN'
    end = data.find('\\', orgn)
    a = data[start:end].split('\n')
    dna = ''
    for i in a:
        spl=i.split()
        dna += ''.join(spl[1:])
    return dna

def find_keyword_locs(data, keyword='   CDS '):
    """Find the number of occurences a keyword appears and extracts them."""
    ngenes = data.count(keyword)
    keylocs = []
    k = 0
    for i in range(ngenes):
        t = data.find(keyword.k)
        keylocs.append(t)
        k = t + 10
    return keylocs
