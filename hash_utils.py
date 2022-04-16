# Jesse Moody - 4/10/2022
# Misc utility functions for working with hashes and hash table files.
# Generate and read hash files. Compute SHA-1 hash.
# External hash files are used so hashes don't have to be recomputed each run.

# Hash tables files:
# simpleHash, doubleHash, tripleHash, numHash, simpleAppendNumHash, tampaPhoneNumHash, dateHash

import hashlib
import copy
from time import perf_counter, perf_counter_ns

# compute SHA-1 hash for given string
def compute_SHA1_hash(string, encoding='utf-8'):
    sha1_hasher = hashlib.sha1()
    sha1_hasher.update(string.encode(encoding))
    return sha1_hasher.hexdigest()

# Don't use for large hash files because reading a hash file usually uses too much memory
# read file containing words and hashes into memory as dictionary
def readHashFile(fileName):
    print(f'Reading {fileName} into memory...', end='')
    dict = {} # create dict object to store test words and their hashes as key/value pairs
    wordList = [] # list for reading dictionary file (without hashes)
    with open(fileName, encoding='utf-8-sig') as f: # using utf-8-sig to remove byte order mark (BOM) <-Google it
        for line in f:
            line = line.split()
            if len(line) > 1:
                word, hash = line
                dict[str(word)] = hash
            else:
                word = line[0]
                wordList.append(word)
    print('Done')
    if dict:
        return dict
    else:
        return wordList

# make simpleHash file with words from dictionary along with respective hashes
# dictionary.txt is a simple txt file with one word per line (no hashes)
def makeSimpleHashTable():
    print('Generating simpleHash...')
    with open('dictionary.txt', 'r', encoding='utf-8-sig') as f, open('simpleHash.txt', 'w') as g:
        for line in f:
            line = line.strip() # strip out newlines. Otherwise, it would be included in hash.
            hash = (compute_SHA1_hash(line)) # calc hash
            g.write(f'{line} {hash}\n')

# make numHash hash file (numeric brute force from 0 to 9,999,999)  
def makeNumHashTable():
    print('Generating numHash file...')
    with open('numHash.txt', 'w') as f:
        percentDone = 0
        for i in range(0, 10000000):
            hash = (compute_SHA1_hash(str(i)))
            f.write(f'{i} {hash}\n')
            if (i != 0) and (i % 500000 == 0):
                percentDone += 5
                print(f'{percentDone}%')
        zeros = '00'
        for i in range(1, 10):  # include multiple zeros since prev range doesn't
            hash = (compute_SHA1_hash(str(i)))
            f.write(f'{zeros} {hash}\n')
            zeros = zeros + '0'
    print('Done')

# make dictionary of phone numbers starting with Tampa area code (813).
# Uses numHash hash file so if that hash file doesn't exist, this will generate it.
def makeTampaPhoneNumHashTable(attempts=0): # pass num of attempts to prevent recursive loop
    if attempts == 2:
        print('Failed to generate tampaPhoneNumDict. Quitting.')
        return
    else:
        print('Generating tampaPhoneNumDict...')
        pass
    try:
        with open('tampaPhoneNumHash.txt', 'w') as f, open('numHash.txt', 'r') as g:
            percentDone = 0
            for line in g:
                num = line.split()[0] # strip newlines and only keep number (not hash)
                numStr = '813'+str(num)
                hash = (compute_SHA1_hash(numStr))
                f.write(f'{numStr} {hash}\n')
                if (int(num) != 0) and (int(num) % 500000 == 0):
                    percentDone += 5
                    print(f'{percentDone}%')
    except: # executes this if numDict couldn't be opened
        print('Need numHash to generate tampaPhoneNumHash.')
        makeNumHashTable()
        print('Done generating numHash.')
        makeTampaPhoneNumHashTable(attempts+1) # ooooo, recursive function! Fancy!
        print('Done')
    
# Make doubleHash hash file (every combination of two words from simpleDict)
def makeDoubleHashTable():
    print('Generating doubleHash...')
    with open('doubleHash.txt', 'w') as f:
        i = 0
        percentDone = 0
        g = readHashFile('dictionary.txt') # read dictionary into memory
        print('Continue generating doubleHash...')
        g2 = copy.deepcopy(g) # copy dictionary so they can be iterated over independantly (probably a more elegant way to do this)
        for word in g: # 1st word
            for appendWord in g2: # 2nd word
                doubleWord = word+appendWord # combine words
                hash = compute_SHA1_hash(doubleWord) # hash
                f.write(f'{doubleWord} {hash}\n') # store combined words with hash in doubleDict
                i+=1
                if i % 1500000 == 0: # this 1,500,000 was precomputed based on how many words will result (~30M)
                    percentDone += 5
                    print(f'{percentDone}%')
    print('Done')


def makeDateHashTable():
    print('Generating dateHash...', end='')
    with open('dateHash.txt', 'w') as f:
        for i in range(1900, 2023):
            for j in range(0, 1232):
                date = str(i) + str(j)
                hash = compute_SHA1_hash(date)
                f.write(f'{date} {hash}\n')
    print('Done')

def makeSimpleAppend3DigitHashTable():
    print('Generating simpleAppend3DigitHash...', end='')
    with open('simpleAppend3DigitHash.txt', 'w') as f:
        i = 0
        percentDone = 0
        g = readHashFile('dictionary.txt') # read dictionary into memory
        print('Continue generating simpleAppend3DigitHash...')
        for word in g:
            for num in range(0,999):
                wordAppendNum = word + str(num)
                hash = compute_SHA1_hash(wordAppendNum) # hash
                f.write(f'{wordAppendNum} {hash}\n') # store with hash in simpleAppend3DigitHash.txt
                i+=1
                if i % 278000 == 0: # precomputed based on total ((5579*999)*0.05=~278K)
                    percentDone += 5
                    print(f'{percentDone}%')
    print('Done')

def speedTest():
    foundPasswords = readHashFile('passwords.txt')
    g1 = readHashFile('dictionary.txt') # read dictionary into memory
    g2 = copy.deepcopy(g1) # copy dictionary so they can be iterated over independantly (probably a more elegant way to do this)
    g3 = copy.deepcopy(g1)
    fakeHash = 'blah'
    foundPasswords = []
    t1 = perf_counter()
    for word1 in g1: # 1st word
        for word2 in g2: # 2nd word
            for word3 in g3:
                tripleWord = word1 + word2 + word3 # combine words
            hash = compute_SHA1_hash(tripleWord) # hash
            if hash == fakeHash:
                foundPasswords[0] = hash
            t2 = perf_counter()
            break
        break
    print(f'Elapsed time = {t2 - t1}')



# create tripleHash (every combination of three words)
#tripleHash = {}
#for word in doubleHash.keys():
#    for appendWord in simpleDict.keys():
#        tripleWord = word+appendWord
#        tripleDict[tripleWord] = (compute_SHA1_hash(tripleWord))

if __name__ == '__main__':
    makeSimpleAppend3DigitHashTable()