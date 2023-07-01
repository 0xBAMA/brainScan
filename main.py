# setup libraries
import tkinter as tk							# display
from PIL import Image, ImageChops, ImageTk		# image manip
import numpy as np								# numerical stuff, for the data array
import random									# something to get some random numbers
import time										# something for timer, tbd

class brainScan_t():
	def __init__( self ):
		self.root = tk.Tk()
		self.root.title( "BrainScan" )

		# create a blank image
		self.dataArray = np.zeros( ( 500, 1000 ) )
		self.arrayImage = Image.fromarray( self.dataArray, mode="RGB" )

		# populate the image with some random data
		# for x in range( 0, 1000 ):
		# 	for y in range( 100, 400 ):
		# 		self.arrayImage.putpixel( ( x, y ), ( random.randint( 0, 255 ), 128, 128 ) )

		self.displayImage = ImageTk.PhotoImage( self.arrayImage ) # create the tk version of it

		# show the image held in img... what is this doing exactly
		self.label = tk.Label( self.root, image = self.displayImage )
		self.label.pack()
		self.update()
		self.root.mainloop()

	def update( self ):
		self.arrayImage = ImageChops.offset( self.arrayImage, 1, 0 ) # shift the image to the right

		# write the new pixel data at the leading edge
		for y in range( 100, 400 ):
			self.arrayImage.putpixel( ( 0, y ), ( random.randint( 0, 255 ), random.randint( 0, 255 ), random.randint( 0, 255 ) ) );

		self.displayImage = ImageTk.PhotoImage( self.arrayImage )
		self.label.configure( image = self.displayImage )
		self.root.after( 16, self.update )

brainScan = brainScan_t()