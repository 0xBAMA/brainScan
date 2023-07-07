#version 430 core

// interpolated vertex color
in vec3 color;

// interpolated vertex position
in vec3 position;

// fragment shader output - this becomes the value for the pixel
out vec4 fragmentColor;

// we know this has been bound to GL_TEXTURE0
layout ( location = 0 ) uniform sampler2D loadedTexture;

// this function runs once for each generated fragment
void main () {

	vec4 texRead = texture( loadedTexture, position.xy );

	// set pixel color to input, fully opaque with alpha == 1.0f
	fragmentColor = vec4( color * texRead.xyz, 1.0f );

}