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
		self.shader = self.createShader( "basic.vs.glsl", "basic.fs.glsl" )
		glUseProgram( self.shader )

		# create the geometry
		self.geo = helloTriangle_t()

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

		running = True
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


class helloTriangle_t():
# ================================================================================================
	def __init__( self ):
# ================================================================================================
		# Hello Triangle x,y,z + r,g,b per vertex
		self.vertices = (
			-0.5, -0.5, 0.0, 1.0, 0.0, 0.0, # red
			 0.5, -0.5, 0.0, 0.0, 1.0, 0.0, # green
			 0.0,  0.5, 0.0, 0.0, 0.0, 1.0, # blue
		)

		# set up to interpret data correctly, as 32-bit floating point
		self.vertices = np.array( self.vertices, dtype=np.float32 )
		self.vertexCount = 3

		# create the vertex array object, kind of a container for buffers
		self.vao = glGenVertexArrays( 1 )
		glBindVertexArray( self.vao )

		# create the vertex buffer object ( holds memory )
		self.vbo = glGenBuffers( 1 )
		glBindBuffer( GL_ARRAY_BUFFER, self.vbo )

		# send the above data ( self.vertices ), internally allocates a buffer on the GPU to hold them
		glBufferData( GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW )

		# set up pointers to the data for the shader to know how to index the data in the buffer
		glEnableVertexAttribArray( 0 ) # 0 is position, 3 floats per vertex, stride of 24 bytes starting at 0
		glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p( 0 ) )
		glEnableVertexAttribArray( 1 ) # 1 is color, 3 floats per vertex, stride of 24 bytes starting at 12
		glVertexAttribPointer( 1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p( 12 ) )

# ================================================================================================
	def destroy( self ):
# ================================================================================================
		# API resource cleanup - weird syntax, expects list type, even though it's a single item here
		glDeleteVertexArrays( 1, ( self.vao, ) )
		glDeleteBuffers( 1, ( self.vbo, ) )


# defines entrypoint to the program? weird
if __name__ == "__main__":
	brainScan = brainScan_t()