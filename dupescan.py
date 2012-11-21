#!/usr/bin/python3
import os
import hashlib
import sys

'''
Peeks around a specified folder and its subfolders checking if any duplicate files exist.
Whether a file is considered a duplicate depends on its contents, not its filename.
'''

location = r"."
database = {}
VERBOSE = False

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
