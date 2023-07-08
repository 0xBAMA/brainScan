# this will be much higher performance than the tkinter version

# https://pyopengl.sourceforge.net/documentation/index.html
# https://pyopengl.sourceforge.net/context/tutorials/index.html

# good tutorial set, easy mapping to the c++ code
# https://www.youtube.com/watch?v=LCK1qdp_HhQ&list=PLn3eTxaOtL2PDnEVNwOgZFm5xYPr4dUoR

# required libs:
# pip install pygame
# pip install pyopengl
# pip install pyopengl_accelerate

import pygame												# some infrastructure, windowing, event handling, etc
from OpenGL.GL import *										# OpenGL API interface
from OpenGL.GL.shaders import compileProgram, compileShader	# for convenience
import numpy as np											# for typed arrays
import ctypes												# for void pointer type, when buffering data
import array												# array data type


class brainScan_t():
# ================================================================================================
	def __init__( self ):
# ================================================================================================
		# initialize windowing stuff
		pygame.init()
		pygame.display.set_mode( ( 640, 480 ), pygame.OPENGL|pygame.DOUBLEBUF )
		self.clock = pygame.time.Clock()

		# set the OpenGL clear color - this is the value written to the color buffer by glClear()
		glClearColor( 0.1, 0.2, 0.2, 1.0 )

		# get the compiled shader, from the files on disk - then set it as the active shader program
		self.shader = self.createShader( "loadingTextures/basic.vs.glsl", "loadingTextures/basic.fs.glsl" )
		glUseProgram( self.shader )

		# create the geometry
		self.geo = quad_t()

		# loading and creating the texture
		self.texture = texture_t()

		# enter the program's main loop
		self.mainLoop()

# ================================================================================================
	def createShader( self, vertexFilepath, fragmentFilepath ):
# ================================================================================================
		# open the vertex shader, read it into a string
		with open( vertexFilepath, 'r' ) as f:
			vertexShaderSource = f.readlines()

		# open the fragment shader, read it into a string
		with open( fragmentFilepath, 'r' ) as f:
			fragmentShaderSource = f.readlines()

		# compile and link the shader stages, into a program we can use to draw with
		shader = compileProgram(
			compileShader( vertexShaderSource, GL_VERTEX_SHADER ),
			compileShader( fragmentShaderSource, GL_FRAGMENT_SHADER )
		)

		return shader


# ================================================================================================
	def mainLoop( self ):
# ================================================================================================
		# loop control
		running = True

		# time offset
		offset = 0.0

		while ( running ):

			# iterate through the event queue
			for event in pygame.event.get():
				if ( event.type == pygame.QUIT ):
					running = False

			# clear the current contents of the screen ( color buffer )
			glClear( GL_COLOR_BUFFER_BIT )

			# set up to draw hello triangle
			glUseProgram( self.shader )
			glBindVertexArray( self.geo.vao )

			# set the texture active
			self.texture.use()

			# pass the time offset to the GPU
			offset = ( offset + 0.001 ) % 1.0
			glUniform1f( glGetUniformLocation( self.shader, "offset" ), offset )

			# draw three vertices, starting at 0 offset in the buffer, interpreted as a triangle
			glDrawArrays( GL_TRIANGLES, 0, self.geo.vertexCount )

			# swap double buffers, to show what's just been drawn
			pygame.display.flip()

			# called once per frame, tells it how long to wait ( 60 fps, waits ~16ms )
			self.clock.tick( 60 )

		# fall out of the loop
		self.quit()

# ================================================================================================
	def quit( self ):
# ================================================================================================
		self.geo.destroy()
		glDeleteProgram( self.shader )
		pygame.quit()


class quad_t():
# ================================================================================================
	def __init__( self ):
# ================================================================================================
		self.vertexArrayData = []

		# this is super ugly, but at this stage not super important

		# point A location, texcoord
		self.vertexArrayData.append( -0.5 )
		self.vertexArrayData.append(  0.5 )
		self.vertexArrayData.append(  0.0 )
		self.vertexArrayData.append(  0.0 )
		self.vertexArrayData.append(  0.0 )

		# point B location, texcoord
		self.vertexArrayData.append(  0.5 )
		self.vertexArrayData.append(  0.5 )
		self.vertexArrayData.append(  0.0 )
		self.vertexArrayData.append(  1.0 )
		self.vertexArrayData.append(  0.0 )

		# point C location, texcoord
		self.vertexArrayData.append( -0.5 )
		self.vertexArrayData.append( -0.5 )
		self.vertexArrayData.append(  0.0 )
		self.vertexArrayData.append(  0.0 )
		self.vertexArrayData.append(  1.0 )

		# point B location, texcoord
		self.vertexArrayData.append(  0.5 )
		self.vertexArrayData.append(  0.5 )
		self.vertexArrayData.append(  0.0 )
		self.vertexArrayData.append(  1.0 )
		self.vertexArrayData.append(  0.0 )

		# point D location, texcoord
		self.vertexArrayData.append(  0.5 )
		self.vertexArrayData.append( -0.5 )
		self.vertexArrayData.append(  0.0 )
		self.vertexArrayData.append(  1.0 )
		self.vertexArrayData.append(  1.0 )

		# point C location, texcoord
		self.vertexArrayData.append( -0.5 )
		self.vertexArrayData.append( -0.5 )
		self.vertexArrayData.append(  0.0 )
		self.vertexArrayData.append(  0.0 )
		self.vertexArrayData.append(  1.0 )

		# set up to interpret data correctly, as 32-bit floating point
		self.vertices = np.array( self.vertexArrayData, dtype=np.float32 )
		self.vertexCount = 6

		# create the vertex array object, kind of a container for buffers
		self.vao = glGenVertexArrays( 1 )
		glBindVertexArray( self.vao )

		# create the vertex buffer object ( holds memory )
		self.vbo = glGenBuffers( 1 )
		glBindBuffer( GL_ARRAY_BUFFER, self.vbo )

		# send the above data ( self.vertices ), internally allocates a buffer on the GPU to hold them
		glBufferData( GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW )

		# set up pointers to the data for the shader to know how to index the data in the buffer
		glEnableVertexAttribArray( 0 ) # 0 is position, 3 floats per vertex, stride of 20 bytes starting at 0
		glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p( 0 ) )
		glEnableVertexAttribArray( 1 ) # 1 is texcoord, 2 floats per vertex, stride of 20 bytes starting at 12
		glVertexAttribPointer( 1, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p( 12 ) )

# ================================================================================================
	def destroy( self ):
# ================================================================================================
		# API resource cleanup - weird syntax, expects list type, even though it's a single item here
		glDeleteVertexArrays( 1, ( self.vao, ) )
		glDeleteBuffers( 1, ( self.vbo, ) )


class texture_t():
# ================================================================================================
	def __init__( self ):
# ================================================================================================
		# create the API resource
		self.texture = glGenTextures( 1 )

		# bind to the GL_TEXTURE_2D bind point
		glBindTexture( GL_TEXTURE_2D, self.texture )

		# create a complete texture - these parameters do not have good defaults
		glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT )
		glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT )
		glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
		glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )

		# load the image from disk, get dimensions, convert to bytes
		image = pygame.image.load( "loadingTextures/test.png" ).convert_alpha()
		imageWidth, imageHeight = image.get_rect().size
		imageData = pygame.image.tostring( image, "RGBA" )

		# send this data to the GPU, via the graphics API
		glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, imageWidth, imageHeight, 0, GL_RGBA, GL_UNSIGNED_BYTE, imageData )

# ================================================================================================
	def use( self ):
# ================================================================================================
		# set the texture unit which subsequent commands will apply to
		glActiveTexture( GL_TEXTURE0 )

		# bind the texture, to the GL_TEXTURE_2D bind point in texture unit 0
		glBindTexture( GL_TEXTURE_2D, self.texture )

# ================================================================================================
	def destroy( self ):
# ================================================================================================
		# API resource cleanup
		glDeleteTextures( 1, ( self.texture, ) )

# defines entrypoint to the program? weird
if __name__ == "__main__":
	brainScan = brainScan_t()