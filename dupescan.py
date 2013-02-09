#!/usr/bin/python3
import os
import hashlib
import sys
import argparse
import re

# regular expression to match hidden files and folders
hiddenFilePattern = re.compile(r'^.*/(.*)')

def printVerbose(message=""):
    if cmdArgs.verbose:
        print(message)

def isHiddenFileFolder(fullFilePath):
    "Determines if a file or folder is considered hidden."
    global hiddenFilePattern
    if bool(hiddenFilePattern.match(fullFilePath)):
        return True
    else:
        return False

def gatherFileNames(startDir,showHiddenFilesDirs=True):
    "Gathers all file names and their paths under a particular folder location. Does not add directories."
    fullFilePaths = []

    for parentDir, childDirs, childFiles in os.walk(startDir):
        #printVerbose(' - ' + parentDir)

        for childFile in childFiles:
            fullFilePath = parentDir + "/" + childFile

            if showHiddenFilesDirs and isHiddenFileFolder(parentDir+'/'+childFile):
                fullFilePaths.append(fullFilePath)
            else:
                fullFilePaths.append(fullFilePath)
            printVerbose(fullFilePath)

    return fullFilePaths

def generateFileHashes(fullFilePaths):
    "Generates a hash(key) for each filename(value) and returns a dictionary with as {hash, <files that match hash>}. Multiple files may exist for one hash."

    for root, dirs, files in os.walk(location):
        printVerbose(' - ' + root)
        for file in files:
            contents = open(root+"/"+file,"rb").read()
            printVerbose("\t+ {0}".format(file))
            hash = hashlib.sha512(contents).hexdigest()

            if hash not in fileHashes:
                fileHashes[hash] = [root+"/"+file]
            else:
                fileHashes[hash].append(root+"/"+file)
        printVerbose() # for newline
    return fileHashes

def getFileHashes(location):
    "Generates a hash for each filename."
    fileHashes = {}

    for root, dirs, files in os.walk(location):
        printVerbose(' - ' + root)
        for file in files:
            contents = open(root+"/"+file,"rb").read()
            printVerbose("\t+ {0}".format(file))
            hash = hashlib.sha512(contents).hexdigest()

            if hash not in fileHashes:
                fileHashes[hash] = [root+"/"+file]
            else:
                fileHashes[hash].append(root+"/"+file)
        printVerbose() # for newline
    return fileHashes

if __name__ == "__main__":
    argsParser = argparse.ArgumentParser(description='Peeks around a specified folder and its subfolders checking if any duplicate files exist.'
            ' Whether a file is considered a duplicate depends on its contents, not its filename. If in non-verbose mode, returns nothing if '
            'there aren\'t any file collisions. Otherwise, it returns the filenames with their paths that contain the same object')
    argsParser.add_argument('-v', '--verbose', help='verbose mode', action='store_true')
    argsParser.add_argument('-hi', '--hidden', help='scans all files including hidden files and folders', action='store_true')
    argsParser.add_argument('location', help='file location of where to begin search', default=os.getcwd(), nargs='?')
    cmdArgs = argsParser.parse_args()

    try:
        printVerbose(" - Checking if any duplicate files exist under \"{0}\"\n".format(cmdArgs.location))
        fileHashes = getFileHashes(cmdArgs.location)
    except Exception as e:
        print("Exception: ", e)

    collisionFound = False
    for fileHash, fileName in fileHashes.items():
        if len(fileName) > 1:
            collisionFound = True
            print("Collision of {0}".format(fileHash))
            for item in fileName:
                print("\t{0}".format(item))
            print()

    if collisionFound == False:
        printVerbose("No collisions detected.")
