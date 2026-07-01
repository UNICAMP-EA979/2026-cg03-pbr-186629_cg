#ifndef LIBRARY_SPECULAR

#define PI 3.14159265359

vec3 specular(vec3 halfAngle, vec3 normal, vec3 lightDirection,
              vec3 viewDirection, float roughness, vec3 fresnel)
{
    float m = pow(2.0, 2.0 * (1.0 - roughness) * 10.0);

    float ndotH = max(0.0, dot(normal, halfAngle));
    float ndotL = max(0.0, dot(normal, lightDirection));
    float ndotV = max(0.0, dot(normal, viewDirection));

    if(ndotL < 0.001 || ndotV < 0.001)
    {
        return vec3(0.0);
    }

    float normalizationFactor = (m + 2.0) / (8.0 * PI);
    float specularTerm = pow(ndotH, m) / (ndotL * ndotV);

    return fresnel * normalizationFactor * specularTerm;
}

float computeSpecular(float fresnel, vec3 normal, vec3 halfAngle,
                      vec3 viewDirection, vec3 lightDirection, float roughness)
{
    return specular(halfAngle, normal, lightDirection,
                    viewDirection, roughness, vec3(fresnel)).r;
}

#define LIBRARY_SPECULAR
#endif
