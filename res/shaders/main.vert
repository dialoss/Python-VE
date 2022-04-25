#version 330

layout (location = 0) in uvec3 vPos;

out vec2 textCoord;
out float textInd;

uniform mat4 view;
uniform mat4 proj;

// gl_Position = projection * view * model * vec4(aPos, 1.0f);

void main(){
    float tx =  float((vPos.z & 0x80000000u) >> 31u);
    float ty =  float((vPos.z & 0x40000000u) >> 30u);
    int ind = int((vPos.z & 0x3FF00000u) >> 20u);
    float z =   float((vPos.z & 0xFFFFFu));
    float x =   float(vPos.x);
    float y =   float((vPos.y & 0xFFFFFu));
    x -= 5e5;
    y -= 5e5;
    z -= 5e5;
    textCoord = vec2(tx, ty);
    textInd = ind;
    gl_Position = proj * view * vec4(x, y, z, 1);
}
