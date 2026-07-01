#version 330 core

#include "light.glsl"

#define MAX_LIGHT 10
#define PI 3.14159265359

//Realiza o sombreamento considerando dados da luz
//Considere f_brdf = 1

in vec3 worldPosition;
in vec3 worldNormal;

out vec4 FragColor;

uniform Light lights[MAX_LIGHT];

void main()
{
    //Calcule a normal do fragmento
    vec3 worldNormalNormalized = normalize(worldNormal);

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


        //Calcule a contribuição da luz e acumule na color
        float cosLambda = max(0.0, dot(worldNormalNormalized, lightDirection));
        vec3 lightContribution = lightColor * attenuation * cosLambda;
        color += lightContribution;
    }

    // Atribua a color para a cor do fragmento
    FragColor = vec4(color, 1.0);
}
