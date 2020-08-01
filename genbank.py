"""Reads the Gene databases and processes the raw data into useful information."""

def parse_DNA(filename):
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