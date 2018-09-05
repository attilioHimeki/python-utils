from PyPDF2 import PdfFileMerger
import os, sys, argparse

def parseArguments():
    parser = argparse.ArgumentParser(description='PDF Merger Parameters')
    parser.add_argument('-V', '--version', action='version', version='0.0.1')
    parser.add_argument("-o", "--output", type=str, default="result.pdf", required = False, help="Output PDF filename", metavar="FILE")
    parser.add_argument("-D", "--dir", type=str, required = True, help="Supplied directory containing PDF files")
    parser.add_argument("-rr", "--recursive", dest='recursive', action='store_true', help="Should navigate the directory recursively?")
    parser.add_argument("-s", "--strict", dest='strict', action='store_true', help="If used, the operation will fail if there are issues with the issued PDF files")
    parser.set_defaults(strict=False)
    return parser.parse_args() 


def applyMerging(args):
    if args.dir:
        pdfDirPath = args.dir
    else:
        pdfDirPath = os.getcwd()

    fileList = os.listdir(pdfDirPath)
    
    if(len(fileList) > 0):
        merger = PdfFileMerger(args.strict)

        for pdf in fileList:
            path = os.path.join(pdfDirPath, pdf)
            if os.path.isfile(path):
                if(isPDFFile(path)):
                    print("Adding " + pdf)
                    merger.append(open(path, 'rb'))
                else:
                    print("Skipping " + pdf)

        finalPath = os.path.join(pdfDirPath, args.output)
        with open(finalPath, 'wb') as pdfOut:
            merger.write(pdfOut)
    else:
        print("The supplied directory is empty")

def isPDFFile(path):
    lowerPath = path.lower()
    return lowerPath.endswith(".pdf")
    

if __name__ == "__main__":
    args = parseArguments()
    applyMerging(args)