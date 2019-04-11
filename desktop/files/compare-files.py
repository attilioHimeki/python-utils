import os, sys, hashlib, argparse

BLOCK_SIZE = 65536

def calculateFileHash(path):
    hasher = hashlib.md5()
    with open(path, 'rb') as targetFile:
        buffer = targetFile.read(BLOCK_SIZE)
        while len(buffer) > 0:
            hasher.update(buffer)
            buffer = targetFile.read(BLOCK_SIZE)
    return hasher.hexdigest()

def isFileNonEmpty(path):
    return os.path.getsize(path) > 0

def processFileHashes(files):
    filesDict = {}
    for path in files:
        if(isFileNonEmpty(path)):
            fileHash = calculateFileHash(path)
            if fileHash in filesDict:
                filesDict[fileHash].append(path)
            else:
                filesDict[fileHash] = [path]
        else:
            print("Skipping empty file " + path)
    return filesDict

def processResult(filesDict):
    values = filesDict.values()
    foundDuplicates = False
    for fileOccurs in values:
        if(len(fileOccurs) > 1):
            fileName = os.path.basename(fileOccurs[0])
            foundDuplicates = True
            print("\nFound duplicate " + fileName + " at:")
            for f in fileOccurs:
                print(f)
    if foundDuplicates == False:
        print("No duplicates found")

def parseArguments():
    parser = argparse.ArgumentParser(description='Compare files Parameters')
    parser.add_argument('-V', '--version', action='version', version='0.0.1')
    parser.add_argument('-f','--files', nargs='+', help='List of files to compare', required=True)
    return parser.parse_args() 

def compareFiles(args):
    if(args.files and len(args.files) > 1):
        files = args.files
        filesDict = processFileHashes(files)
        processResult(filesDict)
    else:
        print("Please supply two or more files using --files")

if __name__ == '__main__':
    args = parseArguments()
    compareFiles(args)