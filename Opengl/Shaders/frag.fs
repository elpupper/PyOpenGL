#version 410 core
in vec2 newTexture;
in vec3 fragNormal;

out vec4 outColor;
uniform sampler2D samplerTexture;

void main()
{
	vec3 ambientLI = vec3(0.3f, 0.2f, 0.4f);
	vec3 sunLI = vec3(0.9f, 0.9f, 0.9f);
	vec3 sunLD = normalize(vec3(0.0f, 0.0f, 2.0f));
	
	vec4 texel = texture(samplerTexture, newTexture);
	
	vec3 LI = ambientLI + sunLI * max(dot(fragNormal, sunLD), 0.0f);
	
    outColor = vec4(texel.rgb * LI, texel.a);
}