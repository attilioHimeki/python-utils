from PyPDF2 import PdfFileWriter, PdfFileReader
import os, sys, argparse

def parseArguments():
    parser = argparse.ArgumentParser(description='PDF Split Parameters')
    parser.add_argument('-V', '--version', action='version', version='0.0.1')
    parser.add_argument("-f", "--file", type=str, required = True, help="Supplied PDF file to manipulate")
    parser.add_argument('-p', '--pages', nargs='+', type=int, required = True, help="List of pages to delete (zero-indexed)")
    return parser.parse_args() 


def applyRemovePages(path, pages):
    if os.path.isfile(path):
        if(isPDFFile(path)):
            sourcePDF = PdfFileReader(open(path, "rb"))
            pathNoExt = os.path.splitext(path)[0]
            numPages = sourcePDF.numPages

            destinationPath = pathNoExt + "_rem.pdf"

            output = PdfFileWriter()

            for i in range(numPages):
                if(i in pages):
                    print("Skipping page %s" % i)
                else:
                    output.addPage(sourcePDF.getPage(i))

            with open(destinationPath, "wb") as outputStream:
                output.write(outputStream)
        else:
            print("File is not a pdf")
    else:
        print("File does not exist")

def isPDFFile(path):
    lowerPath = path.lower()
    return lowerPath.endswith(".pdf")
    

if __name__ == "__main__":
    args = parseArguments()
    applyRemovePages(args.file, args.pages)