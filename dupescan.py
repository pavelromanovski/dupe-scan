#!/usr/bin/python3
import os
import hashlib
import sys
import argparse
import re

# regular expression to match hidden files and folders
hiddenFilePattern = re.compile(r'^.*/(.*)')

def printVerbose(message=""):
    "Prints the console if verbose output is enabled"
    if cmdArgs.verbose:
        print(message)

def stripExtraSlashes(filePath):
    "Strips extra slashes in a filepath"
    return re.sub('/+','/',filePath)

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

    printVerbose(' + Gathering the list of files to be hashed')

    for parentDir, childDirs, childFiles in os.walk(startDir):

        for childFile in childFiles:
            fullFilePath = stripExtraSlashes(parentDir + "/" + childFile)

            if showHiddenFilesDirs and isHiddenFileFolder(parentDir+'/'+childFile):
                fullFilePaths.append(fullFilePath)
            else:
                fullFilePaths.append(fullFilePath)
            printVerbose('   - ' + fullFilePath)

    return fullFilePaths


def generateFileHashes(fullFilePaths):
    "Generates a hash(key) for each filename(value) and returns a dictionary with as {hash, <files that match hash>}. Multiple files may exist for one hash."

    fileHashes = {}

    printVerbose('\n + Generating hashes from the file list')

    for filePath in fullFilePaths:

        fileContents = open(filePath, "rb").read()
        fileHash = hashlib.sha512(fileContents).hexdigest()
        printVerbose("   - {0} [ {1} ] ".format(filePath, fileHash))

        if fileHash in fileHashes:
            fileHashes[fileHash].append(filePath)
        else:
            fileHashes[fileHash] = [filePath]

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
        printVerbose(" + Checking if any duplicate files exist under \"{0}\"\n".format(cmdArgs.location))
        filePaths = gatherFileNames(cmdArgs.location)
        fileHashes = generateFileHashes(filePaths)

        printVerbose("\n + Checking if there are any file duplicates".format(cmdArgs.location))
        fileDuplicates = 0
        for fileHash, filePaths in fileHashes.items():
            if len(filePaths) > 1:
                fileDuplicates += 1
                #print("   - Collision of {0}".format(fileHash))
                print(' Duplicate # ', fileDuplicates)
                for filePath in filePaths:
                    print("\t{0}".format(filePath))
                print()
        if fileDuplicates == 0:
            printVerbose("No collisions detected.")
    except Exception as e:
        print("Exception: ", e)

    sys.exit(1)


