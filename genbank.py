"""Reads the Gene databases and processes the raw data into useful information."""
from os import error
from string import maketrans

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

def gene_locs(data, keylocs):
    """Extracts all of the start and end locations for the genes in the data."""
    genes = []
    for i in range(len(keylocs)):
        #Get this line and look for join or complement.
        end = data.find('\n', keylocs[i])
        temp = data[keylocs[i]: end]
        joinf = 'join' in temp
        compf = 'complement' in temp
        #Get the extracts
        c = 0
        if compf == True: c = 1
        if joinf == True:
            numbs = find_splices(data, keylocs[i])
            genes.append((numbs, compf))
        else:
            sten = easy_start_end(data, keylocs[1], c)
            genes.append(([sten], compf))
    return genes

def complement(st):
    """Function used to extract the coding splices associated with the set complement flag."""
    ##Works for smaller versions.
    #st = st.replace('a', 'T')
    #st = st.replace('t', 'A')
    #st = st.replace('c', 'G')
    #st = st.replace('g', 'C')
    ##Faster when dealing with larger files.
    table = maketrans('acgt', 'tgca')
    st = st.translate(table)
    st = st[::-1]
    return st

def get_coding_dna(dna, genesi):
    """Extracts the coding DNA for a single gene. Uses the original dna string and one member of the list genelocs."""
    #dna from parse_dna
    #genesi is genlocs[i] from gene_locs
    codedna = ''
    N = len(genesi[0]) #number of splices
    for i in range(N):
        st, en = genesi[0][i]
        codedna += dna[st-1:en]
        #Complement flag
        if genesi[1]:
            codedna = complement(codedna)
    return codedna

def get_codons():
    """Creates a dictionary of codons and uses a for loop to lowercase all of the information, and to translate raw dna to it's respective amino acid."""
    CODONS = ( 
        ('ATA','I'), ('ATC','I'), ('ATT','I'), ('ATG','M'), 
        ('ACA','T'), ('ACC','T'), ('ACG','T'), ('ACT','T'), 
        ('AAC','N'), ('AAT','N'), ('AAA','K'), ('AAG','K'), 
        ('AGC','S'), ('AGT','S'), ('AGA','R'), ('AGG','R'),                  
        ('CTA','L'), ('CTC','L'), ('CTG','L'), ('CTT','L'), 
        ('CCA','P'), ('CCC','P'), ('CCG','P'), ('CCT','P'), 
        ('CAC','H'), ('CAT','H'), ('CAA','Q'), ('CAG','Q'), 
        ('CGA','R'), ('CGC','R'), ('CGG','R'), ('CGT','R'), 
        ('GTA','V'), ('GTC','V'), ('GTG','V'), ('GTT','V'), 
        ('GCA','A'), ('GCC','A'), ('GCG','A'), ('GCT','A'), 
        ('GAC','D'), ('GAT','D'), ('GAA','E'), ('GAG','E'), 
        ('GGA','G'), ('GGC','G'), ('GGG','G'), ('GGT','G'), 
        ('TCA','S'), ('TCC','S'), ('TCG','S'), ('TCT','S'), 
        ('TTC','F'), ('TTT','F'), ('TTA','L'), ('TTG','L'), 
        ('TAC','Y'), ('TAT','Y'), ('TAA','p'), ('TAG','p'), 
        ('TGC','C'), ('TGT','C'), ('TGA','p'), ('TGG','W') 
    )
    for i in CODONS:
        codons[i[0].lower()] = i[1]
    return codons

def codons_to_protein(codedna, codons):
    protein = ""
    for i in range(0, len(codedna), 3):
        codon = codedna[i:i+3]
        protein += codons[codon]
    return protein

def get_amino(data, loc):
    """Gets the amino acids from the """
    #Get the amino acids
    trans = data.find('/translation', loc)
    #find the second "
    quot = data.find('"', trans + 15)
    #Extract 
    prot = data[trans+14:quot]
    #Remove newlines and blanks
    prot = prot.replace('\n', '')
    prot = prot.replace(' ','')
    return prot

def decoder_dict():
    """Creates a decoding dictionary"""
    ddct = {}
    ddct['0'] = 'AA'; ddct['1'] = 'AC'; ddct['2'] = 'AG'
    ddct['3'] = 'AT'; ddct['4'] = 'CA'; ddct['5'] = 'CC'
    ddct['6'] = 'CG'; ddct['7'] = 'CT'; ddct['8'] = 'GA'
    ddct['9'] = 'GC'; ddct['A'] = 'GG'; ddct['B'] = 'GT'
    ddct['C'] = 'TA'; ddct['D'] = 'TC'; ddct['E'] = 'TG'
    ddct['F'] = 'TT'
    return ddct

def dna_from_ans1(filename, ddct):
    """Finds the ncba2na tag and the single quotes following the tag, extracts the string within the single quotes and converts the string to ans1."""
    #Read in data
    with open(filename, 'r') as fp:
        a = fp.read()
        fp.close()
    #Extract DNA
    loc = a.find('ncbi2na')
    start = a.find("'", loc) + 1
    end = a.find("'", start+2)
    cpdna = a[start:end] #compressed DNA
    cpdna = cpdna.replace('\n', '')
    #Decode
    dna = ''
    for i in range(len(cpdna)):
        dna += ddct[cpdna[i]]
    return dna
