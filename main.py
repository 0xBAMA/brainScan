# setup libraries
import tkinter as tk						# windowing + display
from PIL import Image, ImageChops, ImageTk	# image creation, manip, pass to tk
import numpy as np							# numerical stuff, for the data array
import random								# something to get some random numbers

class brainScan_t():
# ================================================================================================
	def __init__( self ):
# ================================================================================================
		# create the window
		self.root = tk.Tk()
		self.root.title( "BrainScan" )

		# data size
		self.windowWidth = 1000
		self.windowHeight = 500

		# create a blank PIL Image arrayImage + the corresponding tk ImageTk displayImage
		self.dataArray = np.zeros( ( self.windowHeight, self.windowWidth ) )
		self.arrayImage = Image.fromarray( self.dataArray, mode="RGB" )
		self.displayImage = ImageTk.PhotoImage( self.arrayImage )

		# setup the tkinter label object, to display the ImageTK displayImage
		self.label = tk.Label( self.root, image = self.displayImage )
		self.label.pack() # this is something to do with passing the data, not sure exactly

		# update the data, setup the first update() callback, enter loop
		self.update()
		self.root.mainloop()

# ================================================================================================
	def update( self ):
# ================================================================================================
		# shift the image one pixel to the right
		self.arrayImage = ImageChops.offset( self.arrayImage, 1, 0 )

		# write the new pixel data at the leading edge - replace random data with spectrogram slice
		for y in range( 100, 400 ):
			newData = ( random.randint( 0, 255 ), random.randint( 0, 255 ), random.randint( 0, 255 ) )
			self.arrayImage.putpixel( ( 0, y ), newData )

		# update the contents with the latest data in arrayImage
		self.displayImage = ImageTk.PhotoImage( self.arrayImage )
		self.label.configure( image = self.displayImage )

		# register next update callback, 16ms is for 60fps
		self.root.after( 16, self.update )

# create the object, runs __init__() to initialize, sets up the update callback
brainScan = brainScan_t()