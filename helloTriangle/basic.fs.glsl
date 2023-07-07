#version 430 core

// interpolated vertex position
in vec3 color;

// fragment shader output - this becomes the value for the pixel
out vec4 fragmentColor;

// this function runs once for each generated fragment
void main () {

	// set pixel color to input, fully opaque with alpha == 1.0f
	fragmentColor = vec4( color, 1.0f );

}