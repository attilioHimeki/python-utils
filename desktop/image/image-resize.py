from PIL import Image
import os, sys, argparse

def resize(path, w, h, q=90, f='JPEG', sampleFilter=Image.ANTIALIAS):

    dirs = os.listdir(path)

    for imagePath in dirs:
        fullImagePath = os.path.join(path, imagePath)
        if os.path.isfile(fullImagePath):
            if(isImageFile(fullImagePath)):
                print("Resizing " + fullImagePath)
                image = Image.open(fullImagePath)
                name, ext = os.path.splitext(fullImagePath)
                imResize = image.resize((w, h), sampleFilter)
                imResize.save(name + '_resized.' + f, f, quality=q)
            else:
                print("Skipping " + fullImagePath)


def isImageFile(path):
    lowerPath = path.lower()
    return lowerPath.endswith(".jpg") or lowerPath.endswith(".png") or lowerPath.endswith(".gif") or lowerPath.endswith(".jpeg")


def resizeAspectFit(path, scaleRatio, q=90, f='JPEG', sampleFilter=Image.ANTIALIAS):
    dirs = os.listdir(path)
    for imagePath in dirs:
        fullImagePath = os.path.join(path, imagePath)
        if os.path.isfile(fullImagePath):
            if(isImageFile(fullImagePath)):
                print("Scaling " + fullImagePath)
                image = Image.open(fullImagePath)
                name, ext = os.path.splitext(fullImagePath)
                width, height = image.size
                imResize = image.resize((int(width * scaleRatio), int(height * scaleRatio)), sampleFilter)
                imResize.save(name + '_resized.' + f, f, quality=q)
            else:
                print("Skipping " + fullImagePath)

def parseArguments():
    parser = argparse.ArgumentParser(description='Image Resizer Parameters')
    parser.add_argument('-V', '--version', action='version', version='0.0.1')
    parser.add_argument("-W", "--targetWidth", type=int, help="Saved Image width", required = False, default = -1)
    parser.add_argument("-H", "--targetHeight", type=int, help="Saved Image height", required = False, default = -1)
    parser.add_argument("-S", "--targetScaleRatio", type=float, help="Saved Image scale ratio", required = False, default = 1.0)
    parser.add_argument("-D", "--dir", type=str, help="Supply absolute directory path", required = False, default = "")
    parser.add_argument("-F", "--format", type=str, help="Saved Image format (JPEG, PNG)", required = False, default = "JPEG")
    parser.add_argument("-Q", "--quality", type=int, help="Saved Image quality (0-100)", required = False, default = 100)
    parser.add_argument("-noAA", "--disable-antialias", dest='antialias', action='store_false')
    parser.set_defaults(antialias=True)
    return parser.parse_args() 


def applyResizing(args):
    if args.dir:
        imagesDirPath = args.dir
    else:
        imagesDirPath = os.getcwd()

    if(args.antialias):
        sampleFilter = Image.ANTIALIAS
    else:
        sampleFilter = Image.NEAREST

    if(args.targetScaleRatio != 1.0):
        print("Resizing with target scale ratio " + str(args.targetScaleRatio))
        resizeAspectFit(imagesDirPath, args.targetScaleRatio, args.quality, args.format, sampleFilter)
    else:
        if(args.targetHeight < 1 and args.targetWidth < 1):
            print("Please supply at least one value for width and/or height")
        else:
            print("Resizing with width " + str(args.targetWidth) + " and height " + str(args.targetHeight))
            resize(imagesDirPath, args.targetWidth, args.targetHeight, args.quality, args.format, sampleFilter)
    

if __name__ == "__main__":
    args = parseArguments()
    applyResizing(args)