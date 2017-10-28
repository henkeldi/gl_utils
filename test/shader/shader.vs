#version 450 core

layout (location=0) in vec2 position;
layout (location=1) in vec3 color;
layout (location=2) in vec2 tex_coords;

layout (binding=0) readonly buffer SCENE_BUFFER {
	mat4 view;
	mat4 projection;
	vec3 viewPos;
};

out vec3 vs_color;
out vec2 vs_tex_coords;

void main(){
	gl_Position = projection * view * vec4(position, 0.0, 1.0);
	vs_color = color;
	vs_tex_coords = tex_coords;
}