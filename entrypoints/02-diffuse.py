import numpy as np

import urenderer

# Você deve acrescentar luz difusa ao modelo de sombreamento
#
# Altere os arquivos .../shader_library/fresnel.glsl, .../shader_library/diffuse.glsl
# e 02-fragment.fs para realizar o sombreamento.

if __name__ == "__main__":
    import os
    
    urenderer.utils.clear_workdir("02-diffuse")
    renderer = urenderer.renderer.OpenGLRenderer(1920, 1080)
    renderer.background_color = np.array([0, 0, 0, 1], np.float32)
    runtime = urenderer.application.Runtime(
        renderer, name="02-diffuse")

    # Obter diretorio do script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    vertex_path = os.path.join(script_dir, "vertex.vs")
    fragment_path = os.path.join(script_dir, "02-fragment.fs")
    
    shader = urenderer.renderer.Shader(vertex_path, fragment_path)
    material = urenderer.renderer.opengl.Material(shader)

    sphere = urenderer.node.Node()

    sphere.translation = np.array([0, 0, -5], np.float64)
    sphere.render_data["mesh"] = urenderer.geometry.mesh.get_mesh_sphere()
    sphere.render_data["material"] = material

    runtime.scene.add_child(sphere)

    light = urenderer.node.Light(urenderer.node.LightType.DIRECTIONAL)
    light.rotation = np.array([45, 45, 45], np.float64)
    light.light_intensity = 3.0
    runtime.scene.add_child(light)

    runtime.loop(capture=[1])
