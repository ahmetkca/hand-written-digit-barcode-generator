import cv2
from PIL import Image
import numpy as np
import constants
import os
import math
import matplotlib.pyplot as plt
import time

def create_barcode(imagePath):
    barcode = []

    opcv = cv2.imread(imagePath, 0) # read image file as cv2 image
    ret2, th2 = cv2.threshold(opcv, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) # apply threshold it just makes pixel values either black or white
        
    img = Image.fromarray(th2) # create image from thresholded 2d image array


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
        thresholds.append(int(math.ceil(float(threshold))))
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
                time.sleep(0.5/4)
                if s:
                    successCount += 1
        hitRatio = accuracy(successCount)
        return hitRatio

    def checkSuccess(self, searchBarcode, searchDigitGroup):
        success = False
        minHMD = (constants.IMAGE_SIZE*constants.NUM_PROJECTIONS)+1
        minBarcode = None
        imageLoc = None
        for i, barcode in enumerate(self.barcodes):
            currentHMD = hammingDistance( barcode, searchBarcode)
            if currentHMD == 0:
                continue
            elif currentHMD < minHMD:
                minHMD = currentHMD
                minBarcode = barcode
                imageLoc = self.imageLocations[i]

        resultDigitGroup = imageLoc.split("_", 1)[0]
        if int(resultDigitGroup) == int(searchDigitGroup):
            success = True
        return success, minHMD, imageLoc, minBarcode

class SearchSimilar:
    def __init__(self):
        self.digitSelectMenu()

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

if __name__ == "__main__":
    cahr = CalculateAccuracyHitRatio(barcodes, imageLocations)
    print(cahr.calculateAccuracy())
    # sc = SearchSimilar()

# digitFolder = int(input("enter a digit (0 - 9): "))

# directory = r'.\MNIST_DS\{}'.format(digitFolder)

# for c, imageName in enumerate(os.listdir(directory)):
#     print(c , " - ", imageName)

# selectImage = int(input("select image from above list: "))

# selectedImagePath = os.path.join(directory, os.listdir(directory)[selectImage])

# print(selectedImagePath)

# selectedImageBarcode = create_barcode(selectedImagePath)

# minHMD = (constants.IMAGE_SIZE*constants.NUM_PROJECTIONS)+1
# print(minHMD)
# minBarcode = None
# imageLoc = None
# for i, barcode in enumerate(barcodes):
#     print(imageLocations[i])
#     currentHMD = hammingDistance( barcode,selectedImageBarcode)
#     print(currentHMD)
#     if currentHMD == 0:
#         continue
#     elif currentHMD < minHMD:
#         minHMD = currentHMD
#         minBarcode = barcode
#         imageLoc = imageLocations[i]

# print("Result:")
# print("\tHD: {}".format(minHMD))
# print("\tImage Location: {}".format(imageLoc))
# print("\tBarcode: {}".format(minBarcode))

# fig = plt.figure(figsize=(10, 7))
# fig.suptitle("Hamming Distance: {}".format(minHMD))
# rows, columns = 2, 2

# selectedImage = cv2.imread(selectedImagePath)
# resultImageRelativePath = imageLoc.split("_", 1)
# resultImagePath = os.path.join(r".\MNIST_DS", r"{}\{}".format(resultImageRelativePath[0], resultImageRelativePath[1]))
# resultImage = cv2.imread(resultImagePath)

# from create_barcode_image import BarcodeImageGenerator as big

# big.generate_barcode_image(selectedImageBarcode, r".\temp\searchImage.png")
# big.generate_barcode_image(minBarcode, r".\temp\resultImage.png")

# searchBarcodeImage = cv2.imread(r".\temp\searchImage.png")
# resultBarcodeImage = cv2.imread(r".\temp\resultImage.png")

# fig.add_subplot(rows, columns, 1)

# plt.imshow(selectedImage)
# plt.axis("off")
# plt.title("Search Image")

# fig.add_subplot(rows, columns, 2)

# plt.imshow(resultImage)
# plt.axis("off")
# plt.title("Result Image")

# fig.add_subplot(rows, columns, 3)

# plt.imshow(searchBarcodeImage)
# plt.axis("off")
# plt.title("Search Barcode")

# fig.add_subplot(rows, columns, 4)

# plt.imshow(resultBarcodeImage)
# plt.axis("off")
# plt.title("Result Barcode")

# plt.show()