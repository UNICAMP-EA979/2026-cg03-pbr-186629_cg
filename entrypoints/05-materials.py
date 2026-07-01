import numpy as np
from OpenGL import GL

import urenderer
from urenderer.renderer.opengl import Texture

# Você deve acrescentar suporte para texturas de base color, metallic, roughness
# com tiling ao modelo de sombreamento.
#
# Altere o arquivo 05-fragment.fs

if __name__ == "__main__":
    import os
    
    urenderer.utils.clear_workdir("05-materials")
    renderer = urenderer.renderer.OpenGLRenderer(1920, 1080)
    renderer.background_color = np.array([0, 0, 0, 1], np.float32)
    runtime = urenderer.application.Runtime(
        renderer, name="05-materials")

    renderer.ambient_color = np.array([0.1, 0.1, 0.1], dtype=np.float32)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    vertex_path = os.path.join(script_dir, "vertex.vs")
    fragment_path = os.path.join(script_dir, "05-fragment.fs")
    
    shader = urenderer.renderer.Shader(vertex_path, fragment_path)

    bricks_path = os.path.join(script_dir, "materials", "Bricks104_1K-JPG")
    metal_path = os.path.join(script_dir, "materials", "Metal048A_1K-JPG")

    bricks_base_color = Texture.load_file(
        os.path.join(bricks_path, "Bricks104_1K-JPG_Color.jpg"),
        srgb=True)
    bricks_roughness = Texture.load_file(
        os.path.join(bricks_path, "Bricks104_1K-JPG_Roughness.jpg"))
    bricks_metallic = Texture(np.zeros((1, 1), np.uint8), GL.GL_RED, GL.GL_R8)

    metal_base_color = Texture.load_file(
        os.path.join(metal_path, "Metal048A_1K-JPG_Color.jpg"),
        srgb=True)
    metal_metallic = Texture.load_file(
        os.path.join(metal_path, "Metal048A_1K-JPG_Metalness.jpg"))
    metal_roughness = Texture.load_file(
        os.path.join(metal_path, "Metal048A_1K-JPG_Roughness.jpg"))
    semi_metallic = Texture(200*np.ones((1, 1), np.uint8), GL.GL_RED, GL.GL_R8)

    material1 = urenderer.renderer.opengl.Material(shader)
    material1.set_texture(0, "baseColorTexture", bricks_base_color)
    material1.set_texture(1, "metallicTexture", bricks_metallic)
    material1.set_texture(2, "roughnessTexture", bricks_roughness)
    material1.set_uniform("tiling", 10.0)

    material2 = urenderer.renderer.opengl.Material(shader)
    material2.set_texture(0, "baseColorTexture", bricks_base_color)
    material2.set_texture(1, "metallicTexture", bricks_metallic)
    material2.set_texture(2, "roughnessTexture", bricks_roughness)
    material2.set_uniform("tiling", 1.0)

    material3 = urenderer.renderer.opengl.Material(shader)
    material3.set_texture(0, "baseColorTexture", metal_base_color)
    material3.set_texture(1, "metallicTexture", metal_metallic)
    material3.set_texture(2, "roughnessTexture", metal_roughness)
    material3.set_uniform("tiling", 1.0)

    material4 = urenderer.renderer.opengl.Material(shader)
    material4.set_texture(0, "baseColorTexture", metal_base_color)
    material4.set_texture(1, "metallicTexture", semi_metallic)
    material4.set_texture(2, "roughnessTexture", metal_roughness)
    material4.set_uniform("tiling", 1.0)

    # Cria esferas utilizando os materiais
    sphere1 = urenderer.node.Node()
    sphere1.translation = np.array([-3.5, 0, -5], np.float64)
    sphere1.render_data["mesh"] = urenderer.geometry.mesh.get_mesh_sphere()
    sphere1.render_data["material"] = material1
    runtime.scene.add_child(sphere1)

    sphere2 = sphere1.clone()
    sphere2.translation = np.array([-1.0, 0, -5], np.float64)
    sphere2.render_data["material"] = material2
    runtime.scene.add_child(sphere2)

    sphere3 = sphere1.clone()
    sphere3.translation = np.array([1.0, 0, -5], np.float64)
    sphere3.render_data["material"] = material3
    runtime.scene.add_child(sphere3)

    sphere4 = sphere1.clone()
    sphere4.translation = np.array([3.5, 0, -5], np.float64)
    sphere4.render_data["material"] = material4
    runtime.scene.add_child(sphere4)

    # Luzes
    light = urenderer.node.Light(urenderer.node.LightType.DIRECTIONAL)
    light.rotation = np.array([45, 45, 45], np.float64)
    light.light_intensity = 3.0
    runtime.scene.add_child(light)

    light = urenderer.node.Light(urenderer.node.LightType.DIRECTIONAL)
    light.rotation = np.array([-45, -45, -45], np.float64)
    light.light_intensity = 1.0
    runtime.scene.add_child(light)

    runtime.loop(capture=[1])
