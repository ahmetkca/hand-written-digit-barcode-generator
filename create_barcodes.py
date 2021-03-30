import cv2
from PIL import Image
import numpy as np
import constants
import os
import math

# read thresholds from thresholds.txt and then store them into thresholds list
thresholds = []
with open('./thresholds.txt', 'r') as f:
    threshold = f.readline()
    while threshold:
        threshold = threshold.rstrip("\n")
        # thresholds.append(int(math.ceil(float(threshold))))
        thresholds.append(float(threshold))
        threshold = f.readline()
    f.close()

barcodes = [] # stores every individual barcode for 100 images



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

for currDigit in range(constants.NUMBER_OF_DIGITS): # loop through 0 to NUMBER_OF_DIGITS-1  
    
    directory = r'./MNIST_DS/{}'.format(currDigit) # digit folder path

    for imageName in os.listdir(directory): # loop thorugh every file in the directory
        barcode = create_barcode(os.path.join(directory, imageName))
        barcode.append("{}_{}".format(currDigit, imageName))
        barcodes.append(barcode)

print(len(barcodes))

with open("barcodes.txt", 'w') as f:
    for barcode in barcodes:
        f.write(",".join(str(bit) for bit in barcode) + "\n")
    f.close()

from PIL import Image, ImageDraw

if not os.path.exists('barcodes'):
    os.makedirs('barcodes')

c = 1
for barcode in barcodes:
    barcode.pop()
    im = Image.new('RGB', (len(barcode) * 2, constants.IMAGE_SIZE*constants.NUM_PROJECTIONS), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    px = 0
    for d in barcode:
        if d == 1:
            draw.rectangle((px, 0, px + 2, constants.IMAGE_SIZE*constants.NUM_PROJECTIONS), fill=(0, 0, 0))
        px += 2

    im.save('./barcodes/{}.png'.format(c), quality=100)
    c += 1