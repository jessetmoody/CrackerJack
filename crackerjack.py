# Jesse Moody - 4/10/2022
# Started with code from Nghia Nguyen

import hash_utils as hu
from os.path import exists
import copy

def main():

    foundPasswords = {}
    hashTableFiles = ['simpleHash.txt', 'dateHash.txt', 'numHash.txt', 'tampaPhoneNumHash.txt', 'doubleHash.txt', 'simpleAppend3DigitHash.txt']

    # check if hash files exist and generate them if not (ideally, this would use OOP callback funcs instead)
    if not exists('simpleHash.txt'):
        hu.makeSimpleHashTable()
    if not exists('dateHash.txt'):
        hu.makeDateHashTable()
    if not exists('numHash.txt'):
        hu.makeNumHashTable()
    if not exists('tampaPhoneNumHash.txt'):
        hu.makeTampaPhoneNumHashTable()
    if not exists('doubleHash.txt'):
        hu.makeDoubleHashTable()
    if not exists('simpleAppend3DigitHash.txt'):
        hu.makeSimpleAppend3DigitHashTable()

    passHashes = hu.readHashFile('passwords.txt') # read password hashes into memory
    foundPasswords = copy.deepcopy(passHashes)

    # compare each known hash to each unknown hash
    for hashTable in hashTableFiles: # iterate through dictionary files
        with open(hashTable) as f:
            print(f'\nScanning hashes with {hashTable}')
            for line in f:
                word, hash = line.split()
                for id, passHash in passHashes.items(): # iterate through hashed passwords
                    if hash == passHash:
                        print('Match found!')
                        foundPasswords[id] = word # replace hash with cracked password

    # Display results
    print('Results:\n')
    for id, password in foundPasswords.items():
        print(id + ' ' + password)

if __name__ == '__main__':
    main()