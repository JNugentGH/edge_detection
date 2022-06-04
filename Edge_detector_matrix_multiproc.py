import pyautogui
from PIL import Image
import numpy as np
import multiprocessing
import time

def compute_section(name, pixels_in, size):  
    print("I am process ", name, '\nMy pixel is:', pixels_in[name], '\nSection size: ', size)

##def compute_section(pixels_in, pixels_out):
##    print(name)
##    xoperator = np.matrix('1 0 -1; 2 0 -2; 1 0 -1') # The Sobel Operator Gx
##
##    yoperator = np.matrix('1 2 1; 0 0 0; -1 -2 -1') # Sobel Operator Gy
##
##    w = len(pixels_in)
##    h = len(pixels_in[0])
##    print(w, h)
##    for x in range(1, w-1):
##        for y in range(1, h-1):
##            top = [pixels_in[x+i, y-1] for i in range(-1, 2, 1)]   # Creates a list of the 3 pixels above left, middle and right of the pixel the loop is on.
##            mid = [pixels_in[x+i, y] for i in range(-1, 2, 1)]     #                   "            beside                 "
##            bot = [pixels_in[x+i, y+1] for i in range(-1, 2, 1)]   #   x+(-1), x+(0), x+(1)         below                  "
##
##            pixel_matrix = np.matrix([top, mid, bot])               # Create a numpy matrix with these 3 lists.
##
##            xproduct = (pixel_matrix[0, :]*xoperator[:,0]) + (pixel_matrix[1,:]*xoperator[:,1]) + (pixel_matrix[2,:]*xoperator[:,2]) # Vector multiply the column of our pixels with the row of the mask operator.
##
##            xproduct = abs(int(xproduct))
##            
##            yproduct = (pixel_matrix[0, :]*yoperator[:,0]) + (pixel_matrix[1,:]*yoperator[:,1]) + (pixel_matrix[2,:]*yoperator[:,2])
##
##            yproduct = abs(int(yproduct))
##            
##            mag = np.sqrt( (xproduct*xproduct) + (yproduct*yproduct))
##                    
##            pixels_out[x, y] = (int(mag))

if __name__ == "__main__":
    start_time = time.time()

    xoperator = np.matrix('1 0 -1; 2 0 -2; 1 0 -1') # The Sobel Operator Gx

    yoperator = np.matrix('1 2 1; 0 0 0; -1 -2 -1') # Sobel Operator Gy

    print(xoperator)
    ##screen_cap = pyautogui.screenshot('screenshot.png') # makes pyautogui take a screenshot.

    screen_cap = Image.open("G:\\pyprog\\Robot_Club\\Edge_detector\\kevin_the_carrot.png", 'r')

    flip = screen_cap.transpose(method=Image.FLIP_TOP_BOTTOM) # Uses pillow library to mirror the screenshot upsidedown.

    flip = flip.convert("L")    # Uses pillow library to convert the image to grayscale.

    pixel_data = flip.load()    # Loads the image into a list variable we can change.

    width, height = flip.size   # Gets the images Dimensions.

    print("width: ", width, "\nheight:", height)

    ##stop = 570                 # Controliing variable of how much image to use.

    ##w = (width-1) % stop          # Get our own width dimensions (smaller makes edge detection shorter)
    ##h = (height-1) % stop         # Get our own height.
    w = width-1
    h = height-1

    ##new_image = Image.new("RGB", (w, h), color=0) # Create a new Pillow Image variable that is Greyscale has our width and height in pixels and is all black.
    new_image = Image.new("L", (w, h), color=0) # Create a new Pillow Image variable that is Greyscale has our width and height in pixels and is all black.

    new_data = new_image.load()                     # Load the new image's pixels into a list variable we can edit.

    print(f'W: {w}\nH: {h}\n')                      # Show how Many pixels the new image is. 

    ##for x in range(1, w, 1):                        # Loop through the width.
    ##    for y in range(1, h, 1):                    # Loop through the height for each pixel in the width.
    ##        top = [pixel_data[x+i, y-1] for i in range(-1, 2, 1)]   # Creates a list of the 3 pixels above left, middle and right of the pixel the loop is on.
    ##        mid = [pixel_data[x+i, y] for i in range(-1, 2, 1)]     #                   "            beside                 "
    ##        bot = [pixel_data[x+i, y+1] for i in range(-1, 2, 1)]   #   x+(-1), x+(0), x+(1)         below                  "
    ##
    ##        pixel_matrix = np.matrix([top, mid, bot])               # Create a numpy matrix with these 3 lists.
    ##
    ####        print(pixel_matrix)
    ##        
    ##        xproduct = (pixel_matrix[0, :]*xoperator[:,0]) + (pixel_matrix[1,:]*xoperator[:,1]) + (pixel_matrix[2,:]*xoperator[:,2]) # Vector multiply the column of our pixels with the row of the mask operator.
    ##
    ##        xproduct = abs(int(xproduct))
    ##        
    ##        yproduct = (pixel_matrix[0, :]*yoperator[:,0]) + (pixel_matrix[1,:]*yoperator[:,1]) + (pixel_matrix[2,:]*yoperator[:,2])
    ####        print(product)
    ##        yproduct = abs(int(yproduct))
    ##        
    ##        mag = np.sqrt( (xproduct*xproduct) + (yproduct*yproduct))
    ##                
    ####        new_data[x, y] = (yproduct, xproduct, 0)    # Get the edges in y direction, makes them red and edges in the x direction and makes them grey.
    ##        new_data[x, y] = (int(mag))
    proc_count = 2
    p_width = int((w - (w%proc_count))/proc_count)
    p_height = int((h - (h%proc_count))/proc_count)

    section_size = (p_width, p_height)

    print('pw ph', p_width, p_height)
    x_start = 0
    x_stop = 0
    y_start = 0
    y_stop = 0

    pass_pixels = []
    for i in range(proc_count):
        x_start = x_stop
        x_stop = x_start + p_width -1

        y_start = y_stop
        y_stop = y_start + p_height -1

    ##    if i == proc_count-1:
    ##        x_stop -= w%proc_count
    ##        y_stop -= h%proc_count

        print(x_start, x_stop)
        print(y_start, y_stop)
        print("------------------------")
    ##    p = multiprocessing.Process(target=compute_section, args=(i, pixel_data[x_start:x_stop, y_start:y_stop], new_data[x_start:x_stop, y_start:y_stop],))
        for x in range(x_start, x_stop):
            for y in range(y_start, y_stop):
                pass_pixels.append(int(pixel_data[x, y]))
                
        p = multiprocessing.Process(target=compute_section, args=[i, pass_pixels, section_size])
        p.start()

        x_stop += 1
        
        y_stop += 1

    flip.save('flipped_image_with_red.png')         # Save the coloured screenshot.
    new_image.save('Edges_Detected.png')            # Save the edges that were detected.
    ##new_image.show()                                # Quick view the edges.

    print(time.time() - start_time)
