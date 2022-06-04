from PIL import Image

im = Image.open("christmas_tree.jpg", 'r')

pixels = im.load()

size = im.size

red = Image.new("RGB", size, color=0)
green = Image.new("RGB", size, color=0)
blue = Image.new("RGB", size, color=0)

rejoin = Image.new("RGB", size, color=0)

red_pixels = red.load()
green_pixels = green.load()
blue_pixels = blue.load()

rej_pix = rejoin.load()

for x in range(size[0]):
        for y in range(size[1]):
            red_pixels[x, y] = (pixels[x, y][0]-50, 0, 0)
            
            green_pixels[x, y] = (0, pixels[x, y][1], 0)
            
            blue_pixels[x, y] = (0, 0, pixels[x, y][2]+100)

            rej_pix[x,y] = (pixels[x, y][1], blue_pixels[x, y][2], red_pixels[x,y][0])

red.show()
green.show()
blue.show()

rejoin.show()
