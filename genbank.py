"""Reads the Gene databases and processes the raw data into useful information."""

from os import error


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

def easy_start_end(data, loc, cflag='Normal'):
    """Funtion that finds splice locations for the normal and complement-only cases."""
    #Find the dots
    dots = data.find('..', loc)
    #Targets
    cflag = cflag.lower()
    if cflag is 'normal':
        t1, t2 = ' ', '\n'
    elif cflag is 'complement':
        t1, t2 = '(', ')'
    elif type(cflag) is not str:
        print('InputError: The value that you have assigned to cflag is invalid. \n', 'Value %s is not a valid option, please use either Normal or Complement' % cflag)
    #Find the first preceding blank
    b1 = data.rfind(t1, loc, dots)
    #Find the first following newline
    b2 = data.find(t2, dots)
    #Extract the numbers
    temp = data[b1+1:dots]
    temp = temp.replace('>','')
    temp = temp.replace('<','')
    start = int(temp)
    temp = data[dots+2:b2]
    temp = temp.replace('>','')
    temp = temp.replace('<','')
    end = int(temp)
    return start, end

def find_splices(data, loc):
    """Finds the start and end location of the splice and all intermediate splices based on parentheses, commas, and double periods."""
    #loc is the location of '
    join = data.find('join', loc)
    #Find the parentheses
    p1 = data.find('(', join)
    p2 = data.find(')', join)
    #Count the number of dots
    ndots = data.count('..', p1, p2)
    #Extract the numbers
    numbs = []
    #The First splice has a ( .. ,
    dots = data.find('..', p1)
    t = data[p1+1:dots]
    t = t .replace('<','')
    st = int(t)
    comma = data.find(',', p1)
    en = int(data[dots+2:comma])
    numbs.append((st, en))
    #Consider the rest except the first and last
    #Code is , .. ,
    for i in range(ndots - 2):
        dots = data.find('..', comma)
        comma2 = data.find(',', dots)
        st = int(data[comma+1:dots])
        en = int(data[dots+2:comma2])
        numbs.append((st, en))
    #Last one has code , .. )
    dots = data.find('..', comma)
    st = int(data[comma+1:dots])
    en = int(data[dots+2:p2])
    numbs.append((st, en))
    return numbs
