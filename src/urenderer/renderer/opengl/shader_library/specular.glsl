#ifndef LIBRARY_SPECULAR

#define PI 3.14159265359

//Calcula a refletância especular da superfície utilizando o modelo de Blinn-Phong
float computeSpecular(float fresnel, vec3 normal, vec3 halfAngle, vec3 viewDirection, vec3 lightDirection, float roughness)
{
    // Blinn-Phong BRDF: specular = fresnel * (n+2)/(8*pi) * (n·h)^n
    // onde n = roughness exponent
    // Quanto maior roughness, mais espalhado o brilho especular
    
    // cos(theta_h) = normal · halfAngle
    float cosHalfAngle = max(0.0, dot(normal, halfAngle));
    
    // Converter roughness (0 a 1) para exponent (1 a 256)
    // roughness=0 (brilhante) -> exp=256
    // roughness=1 (fosco) -> exp=1
    float n = mix(256.0, 1.0, roughness * roughness);
    
    // Blinn-Phong: (n·h)^n
    float specularTerm = pow(cosHalfAngle, n);
    
    // Normalizacao Blinn-Phong: (n+2) / (8*pi)
    float normalization = (n + 2.0) / (8.0 * 3.14159265359);
    
    // Combinar: fresnel * normalizacao * (n·h)^n
    // fresnel ja e um float aqui (escalar)
    return fresnel * normalization * specularTerm;
}

#define LIBRARY_SPECULAR
#endif