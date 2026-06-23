#ifndef LIBRARY_FRESNEL

/// Calcula a refletância de Fresnel usando Schlick Approximation
float computeFresnel(float F0, vec3 V, vec3 N)
{
    float cosTheta = max(0.0, dot(V, N));
    float oneMinusCosTheta = 1.0 - cosTheta;
    float fresnel = F0 + (1.0 - F0) * pow(oneMinusCosTheta, 5.0);
    return fresnel;
}

/// Calcula a refletância de Fresnel (versão vetorial)
vec3 fresnelReflectance(vec3 baseColor, float metallic, vec3 halfAngle, vec3 lightDirection)
{
    // Para simplificar, retornar baseColor * (1 - metallic)
    // Em PBR completo, isso seria mais complexo
    return baseColor * (1.0 - metallic);
}

#define LIBRARY_FRESNEL
#endif