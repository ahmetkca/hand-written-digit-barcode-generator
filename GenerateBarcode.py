import constants
from PIL import Image
import cv2
import numpy as np

class GenerateBarcode:

    def __init__(self, thresholds):
        self.thresholds = thresholds

    def create_barcode(self, imagePath):
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
                if row_sum >= self.thresholds[currentProjectionThreshold]: 
                    barcode.append(1)
                else:
                    barcode.append(0)

            degree += constants.STEP_DEGREE

        return barcode