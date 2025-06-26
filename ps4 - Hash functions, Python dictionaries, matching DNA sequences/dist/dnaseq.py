#!/usr/bin/env python2.7

import unittest
from dnaseqlib import *

### Utility classes ###

# Maps integer keys to a set of arbitrary values.
class Multidict:
    """
     Initializes a new multi-value dictionary, and adds any key-value
     2-tuples in the iterable sequence pairs to the data structure.
     
    """
    def __init__(self, pairs=[]):
        #self.pairs = pairs
        self.d = {}
        for pair in pairs:
            self.put(pair[0],pair[1])
    # Associates the value v with the key k.
    def put(self, k, v):
        if k not in self.d.keys():
            self.d[k] = [v]
        else:
            self.d[k].append(v)
        #self.pairs.append((k,v))
    
    # Gets any values that have been associated with the key k; or, if
    # none have been, returns an empty sequence.
    def get(self, k):
        try:
            return self.d[k]
        except KeyError:
            return []    

# Given a sequence of nucleotides, return all k-length subsequences
# and their hashes.  (What else do you need to know about each
# subsequence?)
def subsequenceHashes(seq, k):
    """Given a sequence of nucliotides, returns all k-length subsequences
        To avoid keeping them all in memory at once, the function is implemented
        as a generator.
        
        Input: 
            seq: list???, sequence of nucleutides
        
        Parms:
            k: int, the length of the subsequence
        
        Returns:
            tuple, containing (hashval, (position of subsequence, subsequence))
    """

    try:
        assert k > 0
        subsequence = ''
        for i in range(k):
            subsequence += next(seq)
        pos = 0    
        RH = RollingHash(subsequence)
        # The while loop iterates until next(seq) returns an error which exists
        # the loop.
        while True:
            yield(RH.current_hash(),(pos,subsequence))
            previtm = subsequence[0]
            nextitm = next(seq)
            subsequence = subsequence[1:] + nextitm
            RH.slide(previtm,nextitm)
            pos += 1
    except StopIteration:
        return
    
    
    

# Similar to subsequenceHashes(), but returns one k-length subsequence
# every m nucleotides.  (This will be useful when you try to use two
# whole data files.)
def intervalSubsequenceHashes(seq, k, m):
    """
    Generator function which returns k-length subsequences every m nucleotides. 
    Input:
        seq: iterative string, the DNA sequence which is analysed
        k: int, strig length
        m: int, interval which sequences are hassed.
        
    Returns:
        tuple, containing (hashval, (position of subsequence, subsequence))
    """
    try:
        assert m >= k and k > 0
        # The while loop iterates until next(seq) returns an error which exists
        # the loop.
        pos = 0    
        while True:
            subsequence = ''
            for i in range(k):
                subsequence += next(seq)
            RH = RollingHash(subsequence)
            yield(RH.current_hash(),(pos,subsequence))
            pos += m
            for i in range(m):
                next(seq)
            
    except StopIteration:
        return
    
  
# Searches for commonalities between sequences a and b by comparing
# subsequences of length k.  The sequences a and b should be iterators
# that return nucleotides.  The table is built by computing one hash
# every m nucleotides (for m >= k).
def getExactSubmatches(a, b, k, m):
    """
    Generator which returns commonalities between sequences a and b by comparing
    sequences of length k. 
    
    Input:
        a,b: iterative stringx
        k: int, length of subsequence
    Returns:
        tuple, (position in a, position in b), where the positions indicate the
                begining of the k-length common string in sequences and b.
    """
    # creating a multi-value dictionary for a data set
    d = Multidict(subsequenceHashes(a, k))
    
    for b_hash, (b_pos, b_subseq)  in intervalSubsequenceHashes(b, k,m):     
        # iterating over the list of (pos,seq) which match the hash b_hash
        for a_pos, a_subseq in d.get(b_hash):                
            if b_subseq == a_subseq:
                yield (a_pos,b_pos)
            else:
                continue
    return
    
    
if __name__ == '__main__':

    if len(sys.argv) != 4:
        print('Usage: {0} [file_a.fa] [file_b.fa] [output.png]'.format(sys.argv[0]))
        sys.exit(1)

    # The arguments are, in order: 1) Your getExactSubmatches
    # function, 2) the filename to which the image should be written,
    # 3) a tuple giving the width and height of the image, 4) the
    # filename of sequence A, 5) the filename of sequence B, 6) k, the
    # subsequence size, and 7) m, the sampling interval for sequence
    # A.
    compareSequences(getExactSubmatches, sys.argv[3], (500,500), sys.argv[1], sys.argv[2], 8, 100)
