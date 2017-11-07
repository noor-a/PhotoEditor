# SYSC 1005 A Fall 2015

import sys  # get_image calls exit
from Cimpl import *

def get_image():
    """
    Interactively select an image file and return a Cimpl Image object
    containing the image loaded from the file.
    """

    # Pop up a dialogue box to select a file
    file = choose_file()

    # Exit the program if the Cancel button is clicked.
    if file == "":
        sys.exit("File Open cancelled, exiting program")

    # Open the file containing the image and load it
    img = load_image(file)

    return img

def negative(img):
    """(cimpl.image) -> none
    
    Convert the speicfied image into a colour negative.
    
    >>>image = load_image(choose_file())
    >>>negative(image)
    >>>show(image)
    """
    for pixel in img:
        x, y, col = pixel  
        r, g, b = col
             
        r = 255 - r
        g = 255 - g
        b = 255 - b
        col = create_color(r, g, b)
        set_color(img, x, y, col)
        
def weighted_grayscale(img):
    """(cimpl.image) -> none
    
    Convert the specified image into a greyscale based on teh weighted average of each component in ech pixel.
    
    >>>image = load_image(choose_file())
    >>>weighted_greyscale(image)
    >>>show(image)
    """
    for pixel in img:
            x, y, col = pixel
            r, g, b = col
                   
                           # Use the shade of gray that has the same brightness as the pixel's
                           # original color.
                           
            brightness = r * 0.299 + g * 0.587 + b * 0.114
            gray = create_color(brightness, brightness, brightness)
                           
            set_color(img, x, y, gray)
            
def grayscale(img):
    """ (Cimpl.Image) -> None
    
    Convert the specified picture into a grayscale image.
    
    >>> image = load_image(choose_file()) 
    >>> grayscale(image)
    >>> show(image)        
    """
    
    for pixel in img:
        x, y, col = pixel
        r, g, b = col

        # Use the shade of gray that has the same brightness as the pixel's
        # original color.
        
        brightness = (r + g + b) // 3
        gray = create_color(brightness, brightness, brightness)
        
        set_color(img, x, y, gray)
        
def _adjust_component(amount):
    """ (int) -> int
    
    Divide the range 0..255 into 4 equal sixe quadrants,
    and return the midpoint of the quadrant in which the
    specified amount lies.
    
    >>>_adjust_component(10)
    31
    >>>_adjust_component(85)
    95
    >>>_adjust_component(142)
    159
    >>>_adjust_component(230)
    223
    """
    
    if amount < 64:
        return 31
    if amount < 128:
        return 95
    elif amount < 192:
        return 159
    else:
        return 223
            
def sepia_tint(img):
    """ (cimpl.image) -> none
    
    Convert the specified image to sepia tones.
    
    >>>image = load_image(choose_file())
    >>>sepia_tint(image)
    >>>show(image)
    """
    
    grayscale(img)
        
    for x, y, col in img:
        r, g, b = col
        
        if r < 63:
            r = r * 1.1
            b = b * 0.9
        elif r < 192:                
            r = r * 1.15
            b = b * 0.85           
        else: 
            r = r * 1.08
            b = b * 0.93     
            
        col = create_color(r, g, b)
        set_color(img, x, y, col)
        
def posterize(img):
    """ (cimpl.image) -> none
    
    "Posterize" the specified image.
        
    >>>image = load_image(choose_file())
    >>>posterize(image)
    >>>show(image)
    """
    for pixel in img:
        x, y, col = pixel
        r, g, b = col    
        
        
        col = create_color(_adjust_component(r), _adjust_component(g), _adjust_component(b))
    
        set_color(img, x, y, col)

def detect_edges_better(img,threshold):
    """(Cimpl.Image,float)->None
    
    Modify the specified image using edge detection.
    An edge is detected when apixel's brightness differs
    from the brightness of its neighbours by an amount that
    is greater than the specified threshold.
    
    >>>image=load_image(choose_file())
    >>>detect_edges_better(image)
    >>>show(image)
    """
    
    for y in range(1, get_height(img) - 1):
            for x in range(1, get_width(img) - 1):
                
                # Grab the pixel @(x, y) and its four neighbours
               
                top_red, top_green, top_blue = get_color(img, x, y - 1)
                left_red, left_green, left_blue = get_color(img, x - 1, y)
                bottom_red, bottom_green, bottom_blue = get_color(img, x, y + 1)
                right_red, right_green, right_blue = get_color(img, x + 1, y)
                center_red, center_green, center_blue = get_color(img, x, y)            
                
                average_below = (bottom_red + bottom_green + bottom_blue) // 3
                average_right = (right_red + right_green + right_blue) // 3
                average_center = (center_red + center_green + center_blue) //3
                        
                contrast_center_below = abs(average_center - average_below)
                contrast_center_right = abs(average_center - average_right)
                
                
                if contrast_center_below > threshold or contrast_center_right > threshold:
                    new_color = create_color(0, 0, 0)
                    set_color(img, x, y - 1, new_color)
                    
                else:
                    new_color = create_color(255, 255, 255)
                    set_color(img, x, y - 1, new_color)

# A bit of code to demonstrate how to use get_image().

if __name__ == "__main__":
    done = False
    
    image_loaded = False
    while not done:
        print ( "L)oad image" )
        print ( "N)egative\tG)rayscale\tP)osterize\tS)epia tint\tE)dge detect" )
        print ( "Q)uit" )
    
        command = input("Choose Option (L, N, G, P, S, E, Q): ") 
        
        if command not in ["Q","L","N","G", "P", "S", "E"]:
            print ( "No such command" )         
        elif command == 'Q':
            print ("Exiting" )
            done = True    
    
        elif command == 'L':
            img = get_image()
            image_loaded = True
            show(img)
        
        elif not image_loaded:
            print ("No image Loaded")
            
        elif command == 'N':
            negative(img)
            show(img)
                
        elif command == 'G':
            
            weighted_grayscale(img)
            show(img)
            
        elif command == 'S':
        
            sepia_tint(img)
            show(img)
                
        elif command == 'E':
            
            threshold == input("Threshold Value: ")
            edge_detect(img)
            show(img)
                
        elif command == 'P':
        
            posterize(img)
            show(img)
                       
        
