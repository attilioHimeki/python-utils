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

def getDuplicatesInFolder(folder):
    pathsByHash = {}
    for dirName, subDirs, fileList in os.walk(folder):
        print('Scanning folder ' + dirName)
        for filename in fileList:
            path = os.path.join(dirName, filename)
            if(isFileNonEmpty(path)):
                fileHash = calculateFileHash(path)
                if fileHash in pathsByHash:
                    pathsByHash[fileHash].append(path)
                else:
                    pathsByHash[fileHash] = [path]
            else:
                print("Skipping empty file " + path)
    return pathsByHash

def processResult(pathsByHash):
    values = pathsByHash.values()
    for fileOccurs in values:
        if(len(fileOccurs) > 1):
            fileName= os.path.basename(fileOccurs[0])
            print("\nFound duplicate " + fileName + " at:")
            for f in fileOccurs:
                print(f)

def parseArguments():
    parser = argparse.ArgumentParser(description='Duplicates Finder Parameters')
    parser.add_argument('-V', '--version', action='version', version='0.0.1')
    parser.add_argument("-d", "--dir", help="Supplied directory to navigate", type=str, required = True)
    return parser.parse_args() 

def findDuplicates(args):
    if args.dir:
        folderPath = args.dir
        if os.path.exists(folderPath):
            pathsByHash = getDuplicatesInFolder(folderPath)
            processResult(pathsByHash)
        else:
            print("The supplied directory does not exist")
    else:
        print("Please supply target directory using --dir")

if __name__ == '__main__':
    args = parseArguments()
    findDuplicates(args)