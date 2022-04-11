# Jesse Moody - 4/10/2022
# Started with code from Nghia Nguyen

import hash_utils as hu
from os.path import exists
import copy

def main():

    foundPasswords = {}
    hashDictFiles = ['simpleDict.txt', 'dateDict.txt', 'numDict.txt', 'tampaPhoneNumDict.txt', 'doubleDict.txt']

    # check if hash files exist and generate them if not
    if not exists('simpleDict.txt'):
        hu.makeSimpleDictFile()
    if not exists('dateDict.txt'):
        hu.makeDateDictFile()
    if not exists('numDict.txt'):
        hu.makeNumDictFile()
    if not exists('tampaPhoneNumDict.txt'):
        hu.makeTampaPhoneNumDictFile()
    if not exists('doubleDict.txt'):
        hu.makeDoubleDictFile()

    passHashes = hu.readHashFile('passwords.txt') # read password hashes into memory
    foundPasswords = copy.deepcopy(passHashes)

    # compare each known hash to each unknown hash
    for dictFile in hashDictFiles: # iterate through dictionary files
        with open(dictFile) as f:
            print(f'\nScanning hashes with {dictFile}')
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