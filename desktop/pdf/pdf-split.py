from PyPDF2 import PdfFileWriter, PdfFileReader
import os, sys, argparse

def parseArguments():
    parser = argparse.ArgumentParser(description='PDF Split Parameters')
    parser.add_argument('-V', '--version', action='version', version='0.0.1')
    parser.add_argument("-f", "--file", type=str, required = True, help="Supplied PDF file to split")
    return parser.parse_args() 


def applySplitting(path):
    if os.path.isfile(path):
        if(isPDFFile(path)):
            sourcePDF = PdfFileReader(open(path, "rb"))
            pathNoExt = os.path.splitext(path)[0]
            numPages = sourcePDF.numPages

            if(numPages > 1):
                print("Splitting " + path + " into %s pages" % numPages)

                for i in range(numPages):
                    output = PdfFileWriter()
                    output.addPage(sourcePDF.getPage(i))
                    pageFilePath = pathNoExt + "_page%s.pdf" % i
                    with open(pageFilePath, "wb") as outputStream:
                        output.write(outputStream)
                        print("Adding " + pageFilePath)
            else:
                print("PDF file has only one page")
        else:
            print("File is not a pdf")
    else:
        print("File does not exist")

def isPDFFile(path):
    lowerPath = path.lower()
    return lowerPath.endswith(".pdf")
    

if __name__ == "__main__":
    args = parseArguments()
    applySplitting(args.file)