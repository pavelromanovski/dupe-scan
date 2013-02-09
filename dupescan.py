#!/usr/bin/python3
import os
import hashlib
import sys
import argparse

'''
Peeks around a specified folder and its subfolders checking if any duplicate files exist.
Whether a file is considered a duplicate depends on its contents, not its filename.
'''

location = r"."
database = {}
VERBOSE = False
# contains arguments passed from command line or their defaults in their absence
cmdArgs = None

def printVerbose(text):
    pass

def read_dirs():
    "Reads all files from a given location"
    for root, dirs, files in os.walk(location):
        if VERBOSE == True: print(root)
        for fil in files:
            try:
                contents = open(root+"/"+fil,"rb").read()
                if VERBOSE == True: print("\t{0}".format(fil))
                hash = hashlib.sha512(contents).hexdigest()
            except Exception as e:
                print("Exception: ", e)

            if hash not in database:
                database[hash] = [root+"/"+fil]
            else:
                database[hash].append(root+"/"+fil)
        if VERBOSE == True: print()

if __name__ == "__main__":
    argsParser = argparse.ArgumentParser()
    argsParser.add_argument('-v', '--verbose', help='verbose mode', action='store_true')
    argsParser.add_argument('-a', '--all', help='scans all files including hidden files and folders', action='store_true')
    argsParser.add_argument('location', help='file location of where to begin search', default=r'.', nargs='?')

    cmdArgs = argsParser.parse_args()

    if len(sys.argv) > 1:
        location = sys.argv[1]
    print("Checking if any duplicate files exist under \"{0}\".".format(location))
    try:
        read_dirs()
    except Exception as e:
        print("Exception: ", e)

    collision = False
    for key, value in database.items():
        if len(value) > 1:
            collision = True
            print("Collision of {0}".format(key))
            for item in value:
                print("\t{0}".format(item))
            print()

    if collision == False:
        print("No collisions detected.")
