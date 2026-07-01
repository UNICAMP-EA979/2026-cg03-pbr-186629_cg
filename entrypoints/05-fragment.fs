#version 330 core

#include "light.glsl"
#include "fresnel.glsl"
#include "diffuse.glsl"
#include "specular.glsl"

#define MAX_LIGHT 10
#define PI 3.14159265359

// Adicione suporte para texturas com tiling

in vec3 worldPosition;
in vec3 worldNormal;
in vec2 uv;

uniform vec3 ambientColor;
uniform sampler2D baseColorTexture;
uniform sampler2D metallicTexture;
uniform sampler2D roughnessTexture;
uniform float tiling = 1.0;

out vec4 FragColor;

uniform Light lights[MAX_LIGHT];

void main()
{
    // Calcule a normal do fragmento
    vec3 worldNormalNormalized = normalize(worldNormal);

    // Calcule a direção de visualização (saindo do ponto)
    vec3 viewDirection = normalize(-worldPosition);

    // Calcule a uv com tiling
    vec2 uvTiling = uv * tiling;

    // Realize sampling das texturas para obter as propriedades da superfície
    vec3 baseColor = texture(baseColorTexture, uvTiling).rgb;
    float metallic = texture(metallicTexture, uvTiling).r;
    float roughness = texture(roughnessTexture, uvTiling).r;

    vec3 color = vec3(0);

    // Calcule a luz ambiente
    // Luz ambiente escura para simular luz indireta
    vec3 ambientLightContribution = ambientColor * baseColor;
    color += ambientLightContribution;

    for(int i = 0; i < MAX_LIGHT; i++)
    {
        Light light = lights[i];
        if(light.type == LIGHT_UNSET)
        {
            break;
        }

        //Calcule dados da luz (atenuação, cor, direção)
        float attenuation = computeLightAttenuation(light, worldPosition);
        vec3 lightColor = light.color;
        vec3 lightDirection = computeLightDirection(light, worldPosition);

        //Calcule o half-angle
        vec3 halfAngle = normalize(viewDirection + lightDirection);

        //Calcule as refletância de fresnel, difusa e especular
        float F0 = mix(0.04, 0.95, metallic);
        float fresnel = computeFresnel(F0, viewDirection, worldNormalNormalized);
        vec3 diffuse = computeDiffuse(baseColor, fresnel);
        float specular = computeSpecular(fresnel, worldNormalNormalized, halfAngle, viewDirection, lightDirection, roughness);

        //Calcule a refletância final
        vec3 reflectance = diffuse + vec3(specular);

        //Calcule a contribuição da luz e acumule na color
        float cosLambda = max(0.0, dot(worldNormalNormalized, lightDirection));
        vec3 lightContribution = lightColor * reflectance * attenuation * cosLambda;
        color += lightContribution;
    }

    FragColor = vec4(color, 1.0);
}
