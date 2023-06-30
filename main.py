# setup libraries
import tkinter as tk                            # display
from PIL import Image, ImageChops, ImageTk      # image manip
import numpy as np                              # numerical stuff, for the data array
import random                                   # something to get some random numbers

# create the window
window = tk.Tk()
window.title( 'BrainScan' )

# create a blank image
a = np.zeros( ( 500, 1000 ) )
arrayImage = Image.fromarray( a, mode="RGB" )

# populate the image with some random data
for x in range( 100, 900 ):
    for y in range( 100, 400 ):
        arrayImage.putpixel( ( x, y ), ( random.randint( 0, 255 ), 128, 128 ) )

#shift the image to the right
arrayImage = ImageChops.offset( arrayImage, 100, 0 )

# create the tk version of it
displayImage = ImageTk.PhotoImage( arrayImage )

# show the image held in img... what is this?
lbl = tk.Label( window, image = displayImage ).pack()
# lbl.after( 30, update ) ... there's something with this .after thing, no idea how it works

# how to do something in here? tbd
window.mainloop()

