from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
import os

texture_ids = None
skybox_folder_path = "skybox/"
skybox_texture_paths = list()

def init():
    global skybox_texture_paths
    global texture_ids

    skybox_texture_paths = get_skybox_texture_paths()
    texture_ids = load_cubemap(skybox_texture_paths)

def get_skybox_texture_paths():
    global skybox_folder_path
    global skybox_texture_paths

    cubemap_filenames = [
        "right.png",
        "left.png",
        "top.png",
        "bottom.png",
        "back.png",
        "front.png"
    ]

    skybox_texture_paths = list() 
    
    for filename in cubemap_filenames:
        texture_path = os.path.join(skybox_folder_path, filename).replace("\\","/")
        skybox_texture_paths.append(texture_path)

    return skybox_texture_paths

def load_cubemap(filenames):
    texture_ids = glGenTextures(6)
    for i, filename in enumerate(filenames):
        texture_surface = pygame.image.load(filename)
        texture_data = pygame.image.tostring(texture_surface, "RGB", 1)
        width = texture_surface.get_width()
        height = texture_surface.get_height()

        glBindTexture(GL_TEXTURE_2D, texture_ids[i])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)

    return texture_ids

def draw_skybox(skybox_size):
    global texture_ids

    half_size = skybox_size / 2.0
    
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)

    # Ön yüzey
    glBindTexture(GL_TEXTURE_2D, texture_ids[0])
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-half_size, -half_size, half_size)
    glTexCoord2f(1, 0)
    glVertex3f(half_size, -half_size, half_size)
    glTexCoord2f(1, 1)
    glVertex3f(half_size, half_size, half_size)
    glTexCoord2f(0, 1)
    glVertex3f(-half_size, half_size, half_size)
    glEnd()

    # Arka yüzey
    glBindTexture(GL_TEXTURE_2D, texture_ids[1])
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-half_size, -half_size, -half_size)
    glTexCoord2f(1, 0)
    glVertex3f(half_size, -half_size, -half_size)
    glTexCoord2f(1, 1)
    glVertex3f(half_size, half_size, -half_size)
    glTexCoord2f(0, 1)
    glVertex3f(-half_size, half_size, -half_size)
    glEnd()

    # Üst yüzey
    glBindTexture(GL_TEXTURE_2D, texture_ids[2])
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-half_size, half_size, half_size)
    glTexCoord2f(1, 0)
    glVertex3f(half_size, half_size, half_size)
    glTexCoord2f(1, 1)
    glVertex3f(half_size, half_size, -half_size)
    glTexCoord2f(0, 1)
    glVertex3f(-half_size, half_size, -half_size)
    glEnd()

    # Alt yüzey
    glBindTexture(GL_TEXTURE_2D, texture_ids[3])
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-half_size, -half_size, half_size)
    glTexCoord2f(1, 0)
    glVertex3f(half_size, -half_size, half_size)
    glTexCoord2f(1, 1)
    glVertex3f(half_size, -half_size, -half_size)
    glTexCoord2f(0, 1)
    glVertex3f(-half_size, -half_size, -half_size)
    glEnd()

    # Sol yüzey
    glBindTexture(GL_TEXTURE_2D, texture_ids[4])
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-half_size, -half_size, half_size)
    glTexCoord2f(1, 0)
    glVertex3f(-half_size, -half_size, -half_size)
    glTexCoord2f(1, 1)
    glVertex3f(-half_size, half_size, -half_size)
    glTexCoord2f(0, 1)
    glVertex3f(-half_size, half_size, half_size)
    glEnd()

    # Sağ yüzey
    glBindTexture(GL_TEXTURE_2D, texture_ids[5])
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(half_size, -half_size, half_size)
    glTexCoord2f(1, 0)
    glVertex3f(half_size, -half_size, -half_size)
    glTexCoord2f(1, 1)
    glVertex3f(half_size, half_size, -half_size)
    glTexCoord2f(0, 1)
    glVertex3f(half_size, half_size, half_size)
    glEnd()

    glDisable(GL_TEXTURE_2D)
