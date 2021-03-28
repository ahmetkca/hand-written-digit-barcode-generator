MAX_DEGREE = 180 # Maximum degree you want to rotate the image
MIN_DEGREE = 0 # starting degree it is 0 degree by default
STEP_DEGREE = 22.5 # how many degree you want to increas after each iteration
NUMBER_IMAGES = 10 # Number of images you have in each seperate digit folder
NUMBER_OF_DIGITS = 10 # How many digit folder you have
NUM_PROJECTIONS = int(MAX_DEGREE / STEP_DEGREE) # Calculates number of projections based on maximum degree and step degree
IMAGE_SIZE = 28 # Size of the image so in this case 28 pixel by 28 pixel
