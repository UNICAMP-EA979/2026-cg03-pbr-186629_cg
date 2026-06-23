#ifndef LIBRARY_DIFUSE

#define PI 3.14159265359

//Calcula a refletância difusa da superfície utilizando o modelo de Lambert
vec3 diffuseReflectance(vec3 fresnel, vec3 baseColor, float metallic)
{
    // BRDF Lambertiana: diffuse = baseColor / PI * (1 - fresnel)
    return baseColor / PI * (1.0 - metallic);
}

//Calcula refletância difusa (versão simplificada para computeDiffuse)
vec3 computeDiffuse(vec3 baseColor, float fresnel)
{
    // Aplicar lei de conservação de energia: diffuse = baseColor * (1 - fresnel)
    return baseColor * (1.0 - fresnel);
}

#define LIBRARY_DIFUSE
#endif