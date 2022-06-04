from PIL import Image
import numpy as np
import time
import multiprocessing

def worker(name, l, pixels_in, size, q):
    start = time.time()
    
    l.acquire()
    print(f"I am worker {name}.\n")

    for i in range(10):
        print(pixels_in[i]*name)
    
##    pixels_result =name
    try:
        print(f"{name} has locked.")
        q.put([name, name+1])
        
        
    finally:
##        time.sleep(2)
        l.release()
        print(f"Released after {time.time()-start}")

    print(f"{name} Relesed")

def compute_section(name, l, file_name, section, q):
    print(name)

    artwork = Image.open(file_name, "r")

    grey = artwork.convert("L")

    pixel_data = grey.load()

    width, height = grey.size

##    new_image = Image.new("RGB", (width-1, height-1), color=0) # Create a new Pillow Image variable that is Greyscale has our width and height in pixels and is all black.

    new_image = Image.new("RGB", (section[1]-section[0], height), color=0) # Create a new Pillow Image variable that is Greyscale has our width and height in pixels and is all black.
    
    new_data = new_image.load()                     # Load the new image's pixels into a list variable we can edit.

    xoperator = np.matrix('1 0 -1; 2 0 -2; 1 0 -1') # The Sobel Operator Gx

    yoperator = np.matrix('1 2 1; 0 0 0; -1 -2 -1') # Sobel Operator Gy

##    w = int(size[0])
##    h = int(size[1])
    
##    print(f"w:{w}, h:{h}")
    
    for x in range(section[0], section[1]-1):
        for y in range(1, height-1):
            top = [pixel_data[x+i, y-1] for i in range(-1, 2, 1)]   # Creates a list of the 3 pixels above left, middle and right of the pixel the loop is on.
            mid = [pixel_data[x+i, y] for i in range(-1, 2, 1)]     #                   "            beside                 "
            bot = [pixel_data[x+i, y+1] for i in range(-1, 2, 1)]   #   x+(-1), x+(0), x+(1)         below                  "

            pixel_matrix = np.matrix([top, mid, bot])               # Create a numpy matrix with these 3 lists.

            xproduct = (pixel_matrix[0, :]*xoperator[:,0]) + (pixel_matrix[1,:]*xoperator[:,1]) + (pixel_matrix[2,:]*xoperator[:,2]) # Vector multiply the column of our pixels with the row of the mask operator.

            xproduct = abs(int(xproduct))
            
            yproduct = (pixel_matrix[0, :]*yoperator[:,0]) + (pixel_matrix[1,:]*yoperator[:,1]) + (pixel_matrix[2,:]*yoperator[:,2])

            yproduct = abs(int(yproduct))
            
            mag = np.sqrt( (xproduct*xproduct) + (yproduct*yproduct))

##            new_data[x, y] = (int(mag))
##            new_data[x, y] = (int(mag),int(mag),int(mag))
            new_data[x-section[0], y] = (xproduct, 0, yproduct)

    new_image.save(f"Process_{name}_Output.png")

##    l.acquire()
##
##    try:
##        q.put(pixels_out)
##
##    finally:
##        l.release()

if __name__ == "__main__":
    start_time = time.time()

    file_name = "G:\\pyprog\\Robot_Club\\Edge_detector\\screenshot.png"
##    file_name = "G:\\pyprog\\Robot_Club\\Edge_detector\\leaf.jpg"
##    file_name = "G:\\Phone_Photos\\Bari\\20180825_143759.jpg"

    artwork = Image.open(file_name, "r")

    width, height = artwork.size

    print("width: ", width, "\nheight:", height)

    process_count = 6

    width_remainder = width % process_count
    
    process_width = int((width-width_remainder) / process_count)

    x_start = 0;
    x_stop = 0;
    
    process_pixels = []

    manager = multiprocessing.Manager()

##    pixels_result = manager.list()
    q = multiprocessing.Queue()
    lock = multiprocessing.Lock()
    pixel_result = []

    job_list = []

    for i in range(process_count):
        x_start = x_stop;
        x_stop = x_start + process_width;

##        for x in range(x_start, x_stop):
##            for y in range(height):
##                process_pixels.append(int(pixel_data[x, y]))

        p = multiprocessing.Process(target=compute_section, args=(i, lock, file_name, (x_start, x_stop), q,))

        p.start()
        
        job_list.append(p)

    
    for job in job_list:
        job.join()
##        pixel_result.append(q.get())

    stitch = Image.new("RGB", (width, height), color=0)

    x_off = 0
    
    for i in range(process_count):
        sec = Image.open(f"Process_{i}_Output.png", "r")

        stitch.paste(sec, (x_off, 0))

        sec_w, sec_h = sec.size

        x_off += sec_w

    stitch.save("Multi_Proc_Edge_detect.png")
        

    new_data = pixel_result
    print("Returned")

    end_time = time.time()

    print(f"Time taken to execute: {end_time - start_time}\n")
