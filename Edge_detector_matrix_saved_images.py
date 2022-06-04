##import pyautogui
from PIL import Image
import numpy as np

operator = np.matrix('1 0 -1; 2 0 -2; 1 0 -1') # The Sobel Operator Gx
print(operator)
##screen_cap = pyautogui.screenshot('screenshot.png') # makes pyautogui take a screenshot.

##screen_cap = Image.open("G:\\pyprog\\Robot_Club\\Edge_detector\\leaf.jpg", 'r')
screen_cap = Image.open("G:\\Phone_Photos\\Bari\\20180825_143759.jpg", 'r')


flip = screen_cap.transpose(method=Image.FLIP_TOP_BOTTOM) # Uses pillow library to mirror the screenshot upsidedown.

flip = flip.convert("L")    # Uses pillow library to convert the image to grayscale.

pixel_data = flip.load()    # Loads the image into a list variable we can change.

width, height = flip.size   # Gets the images Dimensions.

stop = 10000                 # Controliing variable of how much image to use.

w = (width-1) % stop          # Get our own width dimensions (smaller makes edge detection shorter)
h = (height-1) % stop         # Get our own height.

new_image = Image.new("RGB", (w, h), color=0) # Create a new Pillow Image variable that is Greyscale has our width and height in pixels and is all black.
new_data = new_image.load()                     # Load the new image's pixels into a list variable we can edit.

print(f'W: {w}\nH: {h}\n')                      # Show how Many pixels the new image is. 

for x in range(1, w, 1):                        # Loop through the width.
    for y in range(1, h, 1):                    # Loop through the height for each pixel in the width.
        top = [pixel_data[x+i, y-1] for i in range(-1, 2, 1)]   # Creates a list of the 3 pixels above left, middle and right of the pixel the loop is on.
        mid = [pixel_data[x+i, y] for i in range(-1, 2, 1)]     #                   "            beside                 "
        bot = [pixel_data[x+i, y+1] for i in range(-1, 2, 1)]   #   x+(-1), x+(0), x+(1)         below                  "

        pixel_matrix = np.matrix([top, mid, bot])               # Create a numpy matrix with these 3 lists.

##        print(pixel_matrix)
        
        product = (pixel_matrix[0, :]*operator[:,0]) + (pixel_matrix[1,:]*operator[:,1]) + (pixel_matrix[2,:]*operator[:,2]) # Vector multiply the column of our pixels with the row of the mask operator.

##        print(product)
        
        new_data[x, y] = (0, abs(int(product)), 0)    # Get the positive value for this.
        
    
flip.save('flipped_image_with_red.png')         # Save the coloured screenshot.
new_image.save('Edges_Detected.png')            # Save the edges that were detected.
new_image.show()                                # Quick view the edges.
