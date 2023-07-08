#version 430 core

layout ( location = 0 ) in vec3 vertexPosition;
layout ( location = 1 ) in vec2 vertexTexcoord;

out vec3 position;
out vec2 texcoord;

// time offset
uniform float offset;

// this function runs once for every input vertex - unique vertex data comes from buffer
void main () {

	// color that will be interpolated between fragments
	position = vertexPosition;
	texcoord = vertexTexcoord + vec2( offset, 0.0f );

	// glsl built in variable for vertex shader output - 4th channel must be 1.0 for now
	gl_Position = vec4( vertexPosition, 1.0f );

}