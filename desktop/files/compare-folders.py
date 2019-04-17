import argparse
from filecmp import dircmp

def compareFolders(args):
    comparisonResult = dircmp(args.sourcedir, args.targetdir)
    if(args.reportmode == 0):
        comparisonResult.report()
    elif(args.reportmode == 1):
        comparisonResult.report_partial_closure()
    elif(args.reportmode == 2):
        comparisonResult.report_full_closure()

def parseArguments():
    parser = argparse.ArgumentParser(description='Compare files Parameters')
    parser.add_argument('-V', '--version', action='version', version='0.0.1')
    parser.add_argument("-s", "--sourcedir", help="Source directory to compare", type=str, required = True)
    parser.add_argument("-t", "--targetdir", help="Target directory to compare", type=str, required = True)
    parser.add_argument("-r", "--reportmode", type=int, help="0:Root only, 1:Include common immediate subdir, 2:Fully Recursive", required = False, default = 0)
    return parser.parse_args() 

if __name__ == '__main__':
    args = parseArguments()
    compareFolders(args)