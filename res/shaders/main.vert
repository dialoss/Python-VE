#version 330

layout (location = 0) in vec3 vPos;
layout (location = 1) in vec2 vTex;
layout (location = 2) in float vInd;

out vec2 textCoord;
out float textInd;

uniform mat4 view;
uniform mat4 proj;

// gl_Position = projection * view * model * vec4(aPos, 1.0f);

void main(){
    textCoord = vTex;
    textInd = vInd;
    gl_Position = proj * view * vec4(vPos, 1);
}
