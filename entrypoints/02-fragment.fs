#version 330 core

#include "light.glsl"
#include "fresnel.glsl"
#include "diffuse.glsl"

#define MAX_LIGHT 10
#define PI 3.14159265359

// Adicione luz difusa ao modelo de sombreamento

in vec3 worldPosition;
in vec3 worldNormal;

out vec4 FragColor;

uniform Light lights[MAX_LIGHT];

void main()
{
    // Calcule a normal do fragmento
    vec3 worldNormalNormalized = normalize(worldNormal);

    //Calcula a direção de visualização (saindo do ponto)
    // Assumindo que camera esta em origem ou usando cameraPosition (será uniform)
    vec3 viewDirection = normalize(-worldPosition);

    vec3 baseColor = vec3(0.5, 0.2, 0.5);
    float metallic = 0;

    vec3 color = vec3(0);
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

        //Calcule as refletância de fresnel e difusa
        float F0 = mix(0.04, 0.95, metallic);
        float fresnel = computeFresnel(F0, viewDirection, worldNormalNormalized);
        vec3 diffuse = computeDiffuse(baseColor, fresnel);

        //Calcule a refletância final
        float cosLambda = max(0.0, dot(worldNormalNormalized, lightDirection));
        vec3 reflectance = diffuse;

        //Calcule a contribuição da luz e acumule na color
        vec3 lightContribution = lightColor * reflectance * attenuation * cosLambda;
        color += lightContribution;
    }

    // Atribua a color para a cor do fragmento
    FragColor = vec4(color, 1.0);
}
