import cv2
import numpy as np

def make_picture(picture:str,x_main:int,y_main:int,black_border_min:int,black_border_max:int,invColour:bool,canny:bool,tLower:int,tUpper:int,canny_type:str):      
    
    img=cv2.imread(picture, cv2.IMREAD_GRAYSCALE)
    if(canny and canny_type=="before black border"):img = cv2.Canny(img,tLower,tUpper)
    img=cv2.resize(img,(x_main,y_main))
    
    example_print=np.zeros((y_main,x_main), dtype=np.uint8)
    white_pixel = 0

    for y,line in enumerate(img):
        for x,pixel in enumerate(line):
            a = pixel >= black_border_min
            b = pixel <= black_border_max
            c = black_border_min < black_border_max
            if  a*b*c + (not c)*(a^b):
                white_pixel+=1
                example_print[y,x]=255

    if(canny and canny_type=="after black border"):example_print = cv2.Canny(example_print,tLower,tUpper)
    
    black_pixel = x_main*y_main-white_pixel
    black_per = (100*black_pixel)/(white_pixel+black_pixel)

    if (invColour):
        example_print = 255 - example_print
        black_per = 100 - black_per
    
    cv2.imwrite("example.tiff", example_print)

    return black_per

def make_gpc(x_main:int,y_main:int,colour:str,black_border_min:int,black_border_max:int,optimization:bool):

    example_print = cv2.imread('example.tiff',cv2.IMREAD_GRAYSCALE) #,cv2.IMREAD_GRAYSCALE

    if(colour == "White"): colour = 1
    else:
        example_print = 255 - example_print
        colour = 0
    #preparing the file
    file= open("myScript.gpc", "w+")
    file.write("init{\nmyPrint()\n}\n\n"
                  +"function myPrint(){\n"
                  +f"cls_oled({1 - colour})\n")
    #+1 from right
    new_column = np.full((y_main, 1), 0 if colour == 0 else 0)
    example_print = np.hstack((example_print, new_column))

    if( optimization):
        for y,line in enumerate(example_print):
            x_count=0
            for x,pixel in enumerate(line):
                if  pixel > 0:
                    x_count+=1
                elif x_count != 0:
                    if x_count > 1:   #line
                        string = f"line_oled({x - x_count}, {y}, {x-1}, {y}, 1, {colour}); "
                    else:             # pixel
                        string = f"pixel_oled({x-1}, {y}, {colour}); "

                    x_count=0
                    file.write(string)

            file.write("\n")
    else:
         for y,line in enumerate(example_print):
            string=""
            for x,pixel in enumerate(line):
                a = pixel >= black_border_min
                b = pixel <= black_border_max
                c = black_border_min < black_border_max
                if  a*b*c + (not c)*(a^b):
                    string += f"pixel_oled({x}, {y}, {colour}); "
              
            file.write(string)
            file.write("\n")

    file.write("}")
    file.close()

