import os, sys, argparse

def parseArguments():
    parser = argparse.ArgumentParser(description='Trim filenames in a directory')
    parser.add_argument('-V', '--version', action='version', version='0.0.1')
    parser.add_argument("-d", "--dir", help="Supplied directory that contains the files", type=str, required = True)
    parser.add_argument("-s", "--start", help="Number of Characters to trim at start", type=int, required = False, default = 0)
    parser.add_argument("-e", "--end", help="Number of Characters to trim at end", type=int, required = False, default = 0)
    parser.add_argument("-r", "--rec", dest='recursive', help="Should navigate subfolders as well", action='store_true')
    parser.set_defaults(recursive=False)
    return parser.parse_args() 

def trimFilename(file, folder, start, end):
    oldPath = os.path.join(folder, file)
    if os.path.isfile(oldPath):
        if(len(file) > start):
            file_noext, ext = os.path.splitext(file)
            endTrim = len(file_noext) - end
            newFileName = file_noext[start:endTrim]
            newPath = os.path.join(folder, newFileName + ext)
            os.rename(oldPath, newPath)
            print("Renamed " + file_noext + " to " + newFileName)
        else:
            print("Cannot trim characters from file " + file + " because it is too short")
    else:
        print("Skipping " + file + " because it is a folder")

    
def trimFilenamesInFolder(folder, start, end):
    for file in os.listdir(folder):
        trimFilename(file, folder, start, end)

def trimFilenamesInFolderRecursive(folder, start, end):
    trimFilenamesInFolder(folder, start, end)
    for dirName, subDirs, fileList in os.walk(folder):
        for folder in subDirs:
            fullFolderPath = os.path.join(dirName, folder)
            trimFilenamesInFolder(fullFolderPath, start, end)

def processTrim(args):
    if args.dir:
        folderPath = args.dir
        if os.path.exists(folderPath):
            if(args.recursive):
                trimFilenamesInFolderRecursive(folderPath, args.start, args.end)
            else:
                trimFilenamesInFolder(folderPath, args.start, args.end)
        else:
            print("The supplied directory does not exist")
    else:
        print("Please supply target directory using --dir")

if __name__ == '__main__':
    args = parseArguments()
    processTrim(args)