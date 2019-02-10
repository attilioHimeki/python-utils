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

def getDuplicatesInFolderByHash(folder):
    filesDict = {}
    for dirName, subDirs, fileList in os.walk(folder):
        print('Scanning folder ' + dirName + " - By hash")
        for filename in fileList:
            path = os.path.join(dirName, filename)
            if(isFileNonEmpty(path)):
                fileHash = calculateFileHash(path)
                if fileHash in filesDict:
                    filesDict[fileHash].append(path)
                else:
                    filesDict[fileHash] = [path]
            else:
                print("Skipping empty file " + path)
    return filesDict

def getDuplicatesInFolderByFilename(folder):
    filesDict = {}
    for dirName, subDirs, fileList in os.walk(folder):
        print('Scanning folder ' + dirName + " - By filename")
        for filename in fileList:
            path = os.path.join(dirName, filename)
            if(isFileNonEmpty(path)):
                if filename in filesDict:
                    filesDict[filename].append(path)
                else:
                    filesDict[filename] = [path]
            else:
                print("Skipping empty file " + path)
    return filesDict

def processResult(filesDict):
    values = filesDict.values()
    foundDuplicates = False
    for fileOccurs in values:
        if(len(fileOccurs) > 1):
            fileName= os.path.basename(fileOccurs[0])
            foundDuplicates = True
            print("\nFound duplicate " + fileName + " at:")
            for f in fileOccurs:
                print(f)
    if foundDuplicates == False:
        print("No duplicates found")

def parseArguments():
    parser = argparse.ArgumentParser(description='Duplicates Finder Parameters')
    parser.add_argument('-V', '--version', action='version', version='0.0.1')
    parser.add_argument("-d", "--dir", help="Supplied directory to navigate", type=str, required = True)
    parser.add_argument("-f", "--byfilename", help="Compare files by filename instead of hash", dest='byfilename', action='store_true')
    parser.set_defaults(byfilename=False)
    return parser.parse_args() 

def findDuplicates(args):
    if args.dir:
        folderPath = args.dir
        if os.path.exists(folderPath):
            if args.byfilename:
                filesDict = getDuplicatesInFolderByFilename(folderPath)
            else:
                filesDict = getDuplicatesInFolderByHash(folderPath)
            processResult(filesDict)
        else:
            print("The supplied directory does not exist")
    else:
        print("Please supply target directory using --dir")

if __name__ == '__main__':
    args = parseArguments()
    findDuplicates(args)