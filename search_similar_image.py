import cv2
from PIL import Image
import numpy as np
import constants
import os
import math
import matplotlib.pyplot as plt
import time


def hammingDistance(v1, v2):
    t = 0
    for i in range(len(v1)):
        if v1[i] != v2[i]:
            t += 1
    return t

# read thresholds from thresholds.txt and then store them into thresholds list
thresholds = []
with open('./thresholds.txt', 'r') as f:
    threshold = f.readline()
    while threshold:
        threshold = threshold.rstrip("\n")
        thresholds.append(float(threshold))
        threshold = f.readline()
    f.close()


# read barcode and image location from barcodes.txt file
imageLocations = []
barcodes = []
with open("barcodes.txt", 'r') as f:
    line = f.readline()
    while line:
        line = line.rstrip("\n")
        line = line.split(",")
        imageLocation = line.pop()
        barcode = []
        for bit in line:
            barcode.append(int(bit))
        imageLocations.append(imageLocation)
        barcodes.append(barcode)
        line = f.readline()
    f.close()

def create_barcode(imagePath):
    barcode = []

    opcv = cv2.imread(imagePath, 0) # read image file as cv2 image
    # ret2, th2 = cv2.threshold(opcv, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) # apply threshold it just makes pixel values either black or white
        
    img = Image.fromarray(opcv) # create image from thresholded 2d image array


    barcode = []
    degree = constants.MIN_DEGREE 
    while degree < constants.MAX_DEGREE: # loop through MIN_DEGREE to MAX_DEGREE by STEP_DEGREE
        currentProjectionThreshold = int(degree / constants.STEP_DEGREE) # find the appropriate threshold index
        rotated_image = img.rotate(degree) # rotate the image
        image2d = np.array(rotated_image) # get 2d representation of the rotated image

            
        for row in image2d:  # loop through each row in thresholded image
            row_sum = 0  # initialize row pixel counter
            for pixel in row: # loop through each pixel in the row
                pixel = pixel / 255  # since we have either 0 or 255 as a pixel value divide this number by 255 to get 0 or 1 which is there is pixel or there is not
                row_sum+=pixel # sum of pixels across a single row
            
            # thresholds the sum of the row to 1 or 0 based on calculated threshold
            if row_sum >= thresholds[currentProjectionThreshold]: 
                barcode.append(1)
            else:
                barcode.append(0)

        degree += constants.STEP_DEGREE

    return barcode

class CalculateAccuracyHitRatio:
    def __init__(self, barcodes, imageLocations):
        self.barcodes = barcodes
        self.imageLocations = imageLocations

    def calculateAccuracy(self):
        accuracy = lambda x : x / 100
        successCount = 0
        for currDigit in range(constants.NUMBER_OF_DIGITS): # loop through 0 to NUMBER_OF_DIGITS-1  
            directory = r'./MNIST_DS/{}'.format(currDigit) # digit folder path
            for imageName in os.listdir(directory): # loop thorugh every file in the directory
                print("Checking image {}".format(os.path.join(directory, imageName)))
                searchBarcode = create_barcode(os.path.join(directory, imageName))
                s, hd, resultImgLoc, resultImgBarcode = self.checkSuccess(searchBarcode, currDigit)
                print("\tHamming Distance: {}\n\tResult Image: {}".format(hd, resultImgLoc))
                # time.sleep(0.5/4)
                if s:
                    successCount += 1
        hitRatio = accuracy(successCount)
        return hitRatio

    def checkSuccess(self, searchBarcode, searchDigitGroup):
        success = False # variable for holding the success information
        minHMD = (constants.IMAGE_SIZE*constants.NUM_PROJECTIONS)+1 # Minimum Hamming Distance. It is (maxiumum hamming distance + 1) by default 
        minBarcode = None # barcode that corresponds to the minimum hamming distance
        imageLoc = None # result image location
        for i, barcode in enumerate(self.barcodes): # loop through every barcode in the barcodes list
            currentHMD = hammingDistance( barcode, searchBarcode) # check each bit in both barcodes and calculate how many of these not same
            if currentHMD == 0: # hamming distance 0 means the barcodes are identical which means they are the same image
                continue # skip
            elif currentHMD < minHMD: # if the current calculated hamming distance is less than the minimum hamming distance 
                minHMD = currentHMD # then set minimum hamming distance to current calculated hamming distance
                minBarcode = barcode # set the current barcode as 
                imageLoc = self.imageLocations[i]

        resultDigitGroup = imageLoc.split("_", 1)[0]
        if int(resultDigitGroup) == int(searchDigitGroup):
            success = True
        return success, minHMD, imageLoc, minBarcode

class SearchSimilar:
    def __init__(self):
        self.digitSelectMenu()

    def findSimilar(self, inputBarcode):
        minHMD = (constants.IMAGE_SIZE*constants.NUM_PROJECTIONS)+1
        print(minHMD)
        minBarcode = None
        imageLoc = None
        for i, barcode in enumerate(barcodes):
            print(imageLocations[i])
            currentHMD = hammingDistance( barcode, inputBarcode)
            print(currentHMD)
            if currentHMD == 0:
                continue
            elif currentHMD < minHMD:
                minHMD = currentHMD
                minBarcode = barcode
                imageLoc = imageLocations[i]
        return minHMD, minBarcode, imageLoc

    def digitSelectMenu(self):
        digitFolder = int(input("enter a digit (0 - 9): "))
        while digitFolder >= 0 and digitFolder <= 9:
            
            directory = r'.\MNIST_DS\{}'.format(digitFolder)

            for c, imageName in enumerate(os.listdir(directory)):
                print(c , " - ", imageName)

            selectImage = int(input("select image from above list: "))

            selectedImagePath = os.path.join(directory, os.listdir(directory)[selectImage])

            print(selectedImagePath)

            selectedImageBarcode = create_barcode(selectedImagePath)

            minHMD = (constants.IMAGE_SIZE*constants.NUM_PROJECTIONS)+1
            print(minHMD)
            minBarcode = None
            imageLoc = None
            for i, barcode in enumerate(barcodes):
                print(imageLocations[i])
                currentHMD = hammingDistance( barcode,selectedImageBarcode)
                print(currentHMD)
                if currentHMD == 0:
                    continue
                elif currentHMD < minHMD:
                    minHMD = currentHMD
                    minBarcode = barcode
                    imageLoc = imageLocations[i]

            print("Result:")
            print("\tHD: {}".format(minHMD))
            print("\tImage Location: {}".format(imageLoc))
            print("\tBarcode: {}".format(minBarcode))

            

            fig = plt.figure(figsize=(10, 7))
            fig.suptitle("Hamming Distance: {}".format(minHMD))
            rows, columns = 2, 2

            selectedImage = cv2.imread(selectedImagePath)
            resultImageRelativePath = imageLoc.split("_", 1)
            resultImagePath = os.path.join(r".\MNIST_DS", r"{}\{}".format(resultImageRelativePath[0], resultImageRelativePath[1]))
            resultImage = cv2.imread(resultImagePath)

            from create_barcode_image import BarcodeImageGenerator as big

            big.generate_barcode_image(selectedImageBarcode, r".\temp\searchImage.png")
            big.generate_barcode_image(minBarcode, r".\temp\resultImage.png")

            searchBarcodeImage = cv2.imread(r".\temp\searchImage.png")
            resultBarcodeImage = cv2.imread(r".\temp\resultImage.png")

            fig.add_subplot(rows, columns, 1)

            plt.imshow(selectedImage)
            plt.axis("off")
            plt.title("Search Image")

            fig.add_subplot(rows, columns, 2)

            plt.imshow(resultImage)
            plt.axis("off")
            plt.title("Result Image")

            fig.add_subplot(rows, columns, 3)

            plt.imshow(searchBarcodeImage)
            plt.axis("off")
            plt.title("Search Barcode")

            fig.add_subplot(rows, columns, 4)

            plt.imshow(resultBarcodeImage)
            plt.axis("off")
            plt.title("Result Barcode")

            plt.show()
            digitFolder = int(input("enter a digit (0 - 9): "))
        
    def showAllResults(self):
        fig = plt.figure(figsize=(16,100), dpi=100)
        rows, cols = constants.NUMBER_OF_DIGITS*constants.NUMBER_IMAGES, 2
        for currDigit in range(constants.NUMBER_OF_DIGITS): # loop through 0 to NUMBER_OF_DIGITS-1  
            directory = r'./MNIST_DS/{}'.format(currDigit) # digit folder path
            for i, imageName in zip((i for i in range(1, 20, 2)), os.listdir(directory)): # loop thorugh every file in the directory
                selectedImagePath = os.path.join(directory, imageName)
                print("Checking image {}".format(os.path.join(directory, imageName)))
                searchBarcode = create_barcode(os.path.join(directory, imageName))
                hmd, resultBarcode, resultImgLoc = self.findSimilar(searchBarcode)
                selectedImage = cv2.imread(selectedImagePath)
                resultImageRelativePath = resultImgLoc.split("_", 1)
                resultImagePath = os.path.join(r".\MNIST_DS", r"{}\{}".format(resultImageRelativePath[0], resultImageRelativePath[1]))
                resultImage = cv2.imread(resultImagePath)

                sii = currDigit*20+i
                fig.add_subplot(rows, cols, sii)
                plt.imshow(selectedImage)
                plt.axis("off")
                plt.title(selectedImagePath, fontsize=9, y=0.90)
                fig.add_subplot(rows, cols, sii+1)
                plt.imshow(resultImage)
                plt.axis("off")
                plt.title(resultImagePath, fontsize=9, y=0.90)
            
        return fig

import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class ScrollableWindow(QtWidgets.QMainWindow):
    def __init__(self, fig):
        self.qapp = QtWidgets.QApplication([])

        QtWidgets.QMainWindow.__init__(self)
        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(QtWidgets.QVBoxLayout())
        self.widget.layout().setContentsMargins(0,0,0,0)
        self.widget.layout().setSpacing(0)

        self.fig = fig
        self.canvas = FigureCanvas(self.fig)
        self.canvas.draw()
        self.scroll = QtWidgets.QScrollArea(self.widget)
        self.scroll.setWidget(self.canvas)

        self.nav = NavigationToolbar(self.canvas, self.widget)
        self.widget.layout().addWidget(self.nav)
        self.widget.layout().addWidget(self.scroll)

        self.show()
        exit(self.qapp.exec_())



if __name__ == "__main__":
    print("Search Menu")
    print("Calculate Accuracy Hit Ratio")
    print("Show All Results at Once")
    input("Yes I have read the above notes. Press Enter to continue...")


    print("\n\n\nEnter a number between 0 and 9 to search image")
    print("Enter a number smaller than 0 or greater than 9 to exit the search menu")
    print("Once you exit Search  Menu you will get Calculate Accuracy Hit Ratio ")
    input("Yes I have read the above notes. Press Enter to continue...")
    si = SearchSimilar() # search menu

    print("\n\n\nCalculating accuracy hit ratio...")
    cahr = CalculateAccuracyHitRatio(barcodes, imageLocations) # accuracy calculator
    print("Accuracy is {}".format(cahr.calculateAccuracy())) # calculate and display the accuracy
    input("Yes I have read the above notes. Press Enter to DISPLAY ALL THE RESULTS at Once...")

    print("\n\n\nSearching all the images in the dataset and finding results...")
    print("Once you get the window maximize the window and scrolldown to see the results")
    input("Yes I have read the above notes. Press Enter to continue...")
    fig = si.showAllResults()
    a = ScrollableWindow(fig)