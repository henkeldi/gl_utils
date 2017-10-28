#version 450 core

#extension GL_NV_bindless_texture : require

layout (location=0) out vec4 color;

in vec3 vs_color;
in vec2 vs_tex_coords;

layout (binding=1, std430) buffer Textures {
	sampler2D samplers[];
};

layout (location=0) uniform int index;

void main(){
	vec3 tex_color = texture(samplers[index], vs_tex_coords).rgb;
	color = vec4(tex_color, 1.0);
}