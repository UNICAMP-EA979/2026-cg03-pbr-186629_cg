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

    # Criar texturas programaticamente
    # Material 1: Liso (low roughness)
    baseColor1 = Texture(np.array([[[255, 100, 100]]], dtype=np.uint8), GL.GL_RGB, GL.GL_RGB8)
    metallic1 = Texture(np.zeros((1, 1), np.uint8), GL.GL_RED, GL.GL_R8)
    roughness1 = Texture(50*np.ones((1, 1), np.uint8), GL.GL_RED, GL.GL_R8)

    material1 = urenderer.renderer.opengl.Material(shader)
    material1.set_texture(0, "baseColorTexture", baseColor1)
    material1.set_texture(1, "metallicTexture", metallic1)
    material1.set_texture(2, "roughnessTexture", roughness1)
    material1.set_uniform("tiling", 1.0)

    # Material 2: Áspero (high roughness)
    baseColor2 = Texture(np.array([[[100, 255, 100]]], dtype=np.uint8), GL.GL_RGB, GL.GL_RGB8)
    metallic2 = Texture(np.zeros((1, 1), np.uint8), GL.GL_RED, GL.GL_R8)
    roughness2 = Texture(200*np.ones((1, 1), np.uint8), GL.GL_RED, GL.GL_R8)

    material2 = urenderer.renderer.opengl.Material(shader)
    material2.set_texture(0, "baseColorTexture", baseColor2)
    material2.set_texture(1, "metallicTexture", metallic2)
    material2.set_texture(2, "roughnessTexture", roughness2)
    material2.set_uniform("tiling", 1.0)

    # Material 3: Metálico
    baseColor3 = Texture(np.array([[[200, 200, 200]]], dtype=np.uint8), GL.GL_RGB, GL.GL_RGB8)
    metallic3 = Texture(255*np.ones((1, 1), np.uint8), GL.GL_RED, GL.GL_R8)
    roughness3 = Texture(100*np.ones((1, 1), np.uint8), GL.GL_RED, GL.GL_R8)

    material3 = urenderer.renderer.opengl.Material(shader)
    material3.set_texture(0, "baseColorTexture", baseColor3)
    material3.set_texture(1, "metallicTexture", metallic3)
    material3.set_texture(2, "roughnessTexture", roughness3)
    material3.set_uniform("tiling", 2.0)

    # Material 4: Semi-metálico (entre metálico e dielétrico)
    baseColor4 = Texture(np.array([[[150, 150, 255]]], dtype=np.uint8), GL.GL_RGB, GL.GL_RGB8)
    metallic4 = Texture(127*np.ones((1, 1), np.uint8), GL.GL_RED, GL.GL_R8)
    roughness4 = Texture(150*np.ones((1, 1), np.uint8), GL.GL_RED, GL.GL_R8)

    material4 = urenderer.renderer.opengl.Material(shader)
    material4.set_texture(0, "baseColorTexture", baseColor4)
    material4.set_texture(1, "metallicTexture", metallic4)
    material4.set_texture(2, "roughnessTexture", roughness4)
    material4.set_uniform("tiling", 1.5)

    # Cria esferas utilizando os materiais
    sphere1 = urenderer.node.Node()
    sphere1.translation = np.array([-3.75, 0, -5], np.float64)
    sphere1.render_data["mesh"] = urenderer.geometry.mesh.get_mesh_sphere()
    sphere1.render_data["material"] = material1
    runtime.scene.add_child(sphere1)

    sphere2 = sphere1.clone()
    sphere2.translation = np.array([-1.25, 0, -5], np.float64)
    sphere2.render_data["material"] = material2
    runtime.scene.add_child(sphere2)

    sphere3 = sphere1.clone()
    sphere3.translation = np.array([1.25, 0, -5], np.float64)
    sphere3.render_data["material"] = material3
    runtime.scene.add_child(sphere3)

    sphere4 = sphere1.clone()
    sphere4.translation = np.array([3.75, 0, -5], np.float64)
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
