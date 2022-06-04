from PIL import Image
import numpy as np

import time

start_time = time.time()

print(f"Start Time:{start_time}")

xoperator = np.matrix('1 0 -1; 2 0 -2; 1 0 -1') # The Sobel Operator Gx
yoperator = np.matrix('1 2 1; 0 0 0; -1 -2 -1') # Sobel Operator Gy
print(yoperator)

screen_cap = Image.open("leaf.png", 'r')
flip = screen_cap

flip = screen_cap.transpose(method=Image.FLIP_TOP_BOTTOM) # Uses pillow library to mirror the screenshot upsidedown.

flip = flip.convert("L")    # Uses pillow library to convert the image to grayscale.

pixel_data = flip.load()    # Loads the image into a list variable we can change.

width, height = flip.size   # Gets the images Dimensions.

w = width-1
h = height-1

##new_image = Image.new("RGB", (w, h), color=0) # Create a new Pillow Image variable that is Greyscale has our width and height in pixels and is all black.
new_image = Image.new("RGB", (w, h), color=0) # Create a new Pillow Image variable that is Greyscale has our width and height in pixels and is all black.

new_data = new_image.load()                     # Load the new image's pixels into a list variable we can edit.

print(f'W: {w}\nH: {h}\n')                      # Show how Many pixels the new image is. 

for x in range(3, w, 1):                        # Loop through the width.
    for y in range(3, h, 1):                    # Loop through the height for each pixel in the width.
        top = [pixel_data[x+i, y-1] for i in range(-1, 2, 1)]   # Creates a list of the 3 pixels above left, middle and right of the pixel the loop is on.
        mid = [pixel_data[x+i, y] for i in range(-1, 2, 1)]     #                   "            beside                 "
        bot = [pixel_data[x+i, y+1] for i in range(-1, 2, 1)]   #   x+(-1), x+(0), x+(1)         below                  "

        pixel_matrix = np.matrix([top, mid, bot])               # Create a numpy matrix with these 3 lists.

##        print(pixel_matrix)
        
##        xproduct = (pixel_matrix[0, :]*xoperator[:,0]) + (pixel_matrix[1,:]*xoperator[:,1]) + (pixel_matrix[2,:]*xoperator[:,2]) # Vector multiply the column of our pixels with the row of the mask operator.
        xproduct = (pixel_matrix[0, :]*xoperator[:,0]) + (pixel_matrix[2,:]*xoperator[:,2]) # Vector multiply the column of our pixels with the row of the mask operator.

        xproduct = abs(int(xproduct))
        
        yproduct = (pixel_matrix[0, 0:3:2]*yoperator[0:3:2,0]) + (pixel_matrix[1,0:3:2]*yoperator[0:3:2,1]) + (pixel_matrix[2,0:3:2]*yoperator[0:3:2,2])
##        yproduct = (pixel_matrix[0, :]*yoperator[:,0]) + (pixel_matrix[1,:]*yoperator[:,1]) + (pixel_matrix[2,:]*yoperator[:,2])

        yproduct = abs(int(yproduct))
        
        mag = np.sqrt( (xproduct*xproduct) + (yproduct*yproduct))
                
        new_data[x, y] = (xproduct, 0, yproduct)    # Get the edges in y direction, makes them red and edges in the x direction and makes them grey.

##        new_data[x, y] = (int(mag))
##        
##        print(pixel_data[x,y])
##
##        print(pixel_matrix)
##
##        print(pixel_matrix[0, :]*yoperator[:,0])
##        print(pixel_matrix[2,:]*yoperator[:,2])
##        
##
##        break
##    break

end_time = time.time()

print(f"Time Taken to run: {end_time-start_time}")

flip.save('flipped_image_with_red.png')         # Save the coloured screenshot.
new_image.save('Edges_Detected.png')            # Save the edges that were detected.
new_image.show()                                # Quick view the edges.
