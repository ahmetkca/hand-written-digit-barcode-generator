import cv2
from PIL import Image
import numpy as np
import constants
import os

projections_thresholds = [] # average of every projections for 100 images

# loop through every digit folder
degree = constants.MIN_DEGREE
while degree < constants.MAX_DEGREE: # loop from MIN_DEGREE to MAX_DEGREE by STEP_DEGREE
    image_mean_sum = 0 # sum of all image means 
    for currDigit in range(constants.NUMBER_OF_DIGITS):
        directory = r'./MNIST_DS/{}'.format(currDigit) # digit folder path

        
        for imageName in os.listdir(directory): # loop thorugh every file in the directory
            print(str(os.path.join(directory, imageName)))
            opcv = cv2.imread(os.path.join(directory, imageName), 0) # read image file as cv2 image
            # ret2, th2 = cv2.threshold(opcv, 0, 255, cv2.THRESH_OTSU) # apply threshold it just makes pixel values either black or white
        
            img = Image.fromarray(opcv) # create image from thresholded 2d image array
            rotated_image = img.rotate(degree) # rotate the image
            image2d = np.array(rotated_image) # get 2d representation of the rotated image
            
            image_sum = 0 # sum of the pixel values across a row
            for row in image2d: # loop over every rows
                for pixel in row: # loop through every pixel in a row
                    pixel = pixel / 255 # since we have either 0 or 255 as a pixel value divide this number by 255 to get 0 or 1 which is there is pixel or there is not
                    image_sum += pixel # sum of pixels
            
            image_mean = image_sum / constants.IMAGE_SIZE # this is the mean of the sum of (the sum of all pixels in a single row)
            image_mean_sum += image_mean # this is the sum of all the values from the previous line
    projection_threshold = image_mean_sum / (constants.NUMBER_OF_DIGITS * len(os.listdir(directory))) # this is the mean previous line 
    projections_thresholds.append(projection_threshold)
    degree += constants.STEP_DEGREE # increment degree by STEP_DEGREE


# write the calculated thresholds to a file called thresholds.txt
with open("thresholds.txt", 'w') as f:
    for projection_threshold in projections_thresholds:
        f.write(str(projection_threshold) + "\n")
    f.close()