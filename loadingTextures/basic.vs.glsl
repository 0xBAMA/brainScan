#version 430 core

layout ( location = 0 ) in vec3 vertexPosition;
layout ( location = 1 ) in vec3 vertexColor;

out vec3 color;
out vec3 position;

// this function runs once for every input vertex - unique vertex data comes from buffer
void main () {

	// color that will be interpolated between fragments
	color = vertexColor;
	position = vertexPosition;

	// glsl built in variable for vertex shader output - 4th channel must be 1.0 for now
	gl_Position = vec4( vertexPosition, 1.0f );

}