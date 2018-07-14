import os, operator, sys, argparse

def formatFileSize(num):
    for label in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, label)
        num /= 1024.0

def listFilesSize(args):
    if args.dir:
        folderPath = args.dir
        if os.path.exists(folderPath):
            filesWithSize = getSortedFilesListWithSize(folderPath)
            for fi in filesWithSize:
                print(fi[0], formatFileSize(fi[1]))
        else:
            print("The supplied directory does not exist")
    else:
        print("Please supply target directory using --dir")


def getSortedFilesListWithSize(folderPath):
    filesList =  (os.path.join(basedir, filename) for basedir, dirs, files in os.walk(folderPath) for filename in files)
    filesWithSize = ((path, os.path.getsize(path)) for path in filesList)
    filesWithSize = sorted(filesWithSize, key = operator.itemgetter(1), reverse=True)
    return filesWithSize

def parseArguments():
    parser = argparse.ArgumentParser(description='Files Size List')
    parser.add_argument('-V', '--version', action='version', version='0.0.1')
    parser.add_argument("-d", "--dir", help="Supplied directory to analyze", type=str, required = True)
    return parser.parse_args() 

if __name__ == '__main__':
    args = parseArguments()
    listFilesSize(args)