from ctypes import windll
import itertools
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import sound
import skybox
from PIL import Image

objects_for_collision = []
obstacles_for_collision = []
font = 0

class Font:
    def __init__(self):
        #some parameters for fine tuning.
        w = 55.55 / 1000.0
        h =  63.88 / 1150.0
        heightOffset = 8.5 / 1150.0
        margin = 0.014

        """
            Letter: (left, top, width, height)
        """
        self.letterTexCoords = {
            'A': (       w, 1.0 - h,                          w - margin, h - margin), 'B': ( 3.0 * w, 1.0 - h,                          w - margin, h - margin),
            'C': ( 5.0 * w, 1.0 - h,                          w - margin, h - margin), 'D': ( 7.0 * w, 1.0 - h,                          w - margin, h - margin),
            'E': ( 9.0 * w, 1.0 - h,                          w - margin, h - margin), 'F': (11.0 * w, 1.0 - h,                          w - margin, h - margin),
            'G': (13.0 * w, 1.0 - h,                          w - margin, h - margin), 'H': (15.0 * w, 1.0 - h,                          w - margin, h - margin),
            'I': (17.0 * w, 1.0 - h,                          w - margin, h - margin), 'J': (       w, 1.0 - 3.0 * h + heightOffset,     w - margin, h - margin),
            'K': ( 3.0 * w, 1.0 - 3.0 * h + heightOffset,     w - margin, h - margin), 'L': ( 5.0 * w, 1.0 - 3.0 * h + heightOffset,     w - margin, h - margin),
            'M': ( 7.0 * w, 1.0 - 3.0 * h + heightOffset,     w - margin, h - margin), 'N': ( 9.0 * w, 1.0 - 3.0 * h + heightOffset,     w - margin, h - margin),
            'O': (11.0 * w, 1.0 - 3.0 * h + heightOffset,     w - margin, h - margin), 'P': (13.0 * w, 1.0 - 3.0 * h + heightOffset,     w - margin, h - margin),
            'Q': (15.0 * w, 1.0 - 3.0 * h + heightOffset,     w - margin, h - margin), 'R': (17.0 * w, 1.0 - 3.0 * h + heightOffset,     w - margin, h - margin),
            'S': (       w, 1.0 - 5.0 * h + 2 * heightOffset, w - margin, h - margin), 'T': ( 3.0 * w, 1.0 - 5.0 * h + 2 * heightOffset, w - margin, h - margin),
            'U': ( 5.0 * w, 1.0 - 5.0 * h + 2 * heightOffset, w - margin, h - margin), 'V': ( 7.0 * w, 1.0 - 5.0 * h + 2 * heightOffset, w - margin, h - margin),
            'W': ( 9.0 * w, 1.0 - 5.0 * h + 2 * heightOffset, w - margin, h - margin), 'X': (11.0 * w, 1.0 - 5.0 * h + 2 * heightOffset, w - margin, h - margin),
            'Y': (13.0 * w, 1.0 - 5.0 * h + 2 * heightOffset, w - margin, h - margin), 'Z': (15.0 * w, 1.0 - 5.0 * h + 2 * heightOffset, w - margin, h - margin),

            'a': (       w,                     1.0 - 7.0 * h, w - margin, h - margin), 'b': ( 3.0 * w,         1.0 - 7.0 * h, w - margin, h - margin),
            'c': ( 5.0 * w,                     1.0 - 7.0 * h, w - margin, h - margin), 'd': ( 7.0 * w,         1.0 - 7.0 * h, w - margin, h - margin),
            'e': ( 9.0 * w,                     1.0 - 7.0 * h, w - margin, h - margin), 'f': (11.0 * w,         1.0 - 7.0 * h, w - margin, h - margin),
            'g': (13.0 * w,                     1.0 - 7.0 * h, w - margin, h - margin), 'h': (15.0 * w,         1.0 - 7.0 * h, w - margin, h - margin),
            'i': (17.0 * w,                     1.0 - 7.0 * h, w - margin, h - margin), 'j': (       w,      1.0 - 9.0 * h + heightOffset, w - margin, h - margin),
            'k': ( 3.0 * w,      1.0 - 9.0 * h + heightOffset, w - margin, h - margin), 'l': ( 5.0 * w,      1.0 - 9.0 * h + heightOffset, w - margin, h - margin),
            'm': ( 7.0 * w,      1.0 - 9.0 * h + heightOffset, w - margin, h - margin), 'n': ( 9.0 * w,      1.0 - 9.0 * h + heightOffset, w - margin, h - margin),
            'o': (11.0 * w,      1.0 - 9.0 * h + heightOffset, w - margin, h - margin), 'p': (13.0 * w,      1.0 - 9.0 * h + heightOffset, w - margin, h - margin),
            'q': (15.0 * w,      1.0 - 9.0 * h + heightOffset, w - margin, h - margin), 'r': (17.0 * w,      1.0 - 9.0 * h + heightOffset, w - margin, h - margin),
            's': (       w, 1.0 - 11.0 * h + 2 * heightOffset, w - margin, h - margin), 't': ( 3.0 * w, 1.0 - 11.0 * h + 2 * heightOffset, w - margin, h - margin),
            'u': ( 5.0 * w, 1.0 - 11.0 * h + 2 * heightOffset, w - margin, h - margin), 'v': ( 7.0 * w, 1.0 - 11.0 * h + 2 * heightOffset, w - margin, h - margin),
            'w': ( 9.0 * w, 1.0 - 11.0 * h + 2 * heightOffset, w - margin, h - margin), 'x': (11.0 * w, 1.0 - 11.0 * h + 2 * heightOffset, w - margin, h - margin),
            'y': (13.0 * w, 1.0 - 11.0 * h + 2 * heightOffset, w - margin, h - margin), 'z': (15.0 * w, 1.0 - 11.0 * h + 2 * heightOffset, w - margin, h - margin),

            '0': (       w, 1.0 - 13.0 * h, w - margin, h - margin), '1':  ( 3.0 * w,                1.0 - 13.0 * h, w - margin, h - margin),
            '2': ( 5.0 * w, 1.0 - 13.0 * h, w - margin, h - margin), '3':  ( 7.0 * w,                1.0 - 13.0 * h, w - margin, h - margin),
            '4': ( 9.0 * w, 1.0 - 13.0 * h, w - margin, h - margin), '5':  (11.0 * w,                1.0 - 13.0 * h, w - margin, h - margin),
            '6': (13.0 * w, 1.0 - 13.0 * h, w - margin, h - margin), '7':  (15.0 * w,                1.0 - 13.0 * h, w - margin, h - margin),
            '8': (17.0 * w, 1.0 - 13.0 * h, w - margin, h - margin), '9':  (       w, 1.0 - 15.0 * h + heightOffset, w - margin, h - margin),
            
            '.':  ( 3.0 * w,     1.0 - 15.0 * h + heightOffset, w - margin, h - margin), ',': ( 5.0 * w,     1.0 - 15.0 * h + heightOffset, w - margin, h - margin),
            ';':  ( 7.0 * w,     1.0 - 15.0 * h + heightOffset, w - margin, h - margin), ':': ( 9.0 * w,     1.0 - 15.0 * h + heightOffset, w - margin, h - margin),
            '$':  (11.0 * w,     1.0 - 15.0 * h + heightOffset, w - margin, h - margin), '#': (13.0 * w,     1.0 - 15.0 * h + heightOffset, w - margin, h - margin),
            '\'': (15.0 * w,     1.0 - 15.0 * h + heightOffset, w - margin, h - margin), '!': (17.0 * w,     1.0 - 15.0 * h + heightOffset, w - margin, h - margin),
            '"':  (       w, 1.0 - 17.0 * h + 2 * heightOffset, w - margin, h - margin), '/': ( 3.0 * w, 1.0 - 17.0 * h + 2 * heightOffset, w - margin, h - margin),
            '?':  ( 5.0 * w, 1.0 - 17.0 * h + 2 * heightOffset, w - margin, h - margin), '%': ( 7.0 * w, 1.0 - 17.0 * h + 2 * heightOffset, w - margin, h - margin),
            '&':  ( 9.0 * w, 1.0 - 17.0 * h + 2 * heightOffset, w - margin, h - margin), '(': (11.0 * w, 1.0 - 17.0 * h + 2 * heightOffset, w - margin, h - margin),
            ')':  (13.0 * w, 1.0 - 17.0 * h + 2 * heightOffset, w - margin, h - margin), '@': (15.0 * w, 1.0 - 17.0 * h + 2 * heightOffset, w - margin, h - margin)
        }

        self.texture = load_texture("texture/Inconsolata.png")

        # self.texture = glGenTextures(1)
        # glBindTexture(GL_TEXTURE_2D, self.texture)
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_LINEAR)
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        # with Image.open("texture/Inconsolata.png", mode = "r") as img:
        #     image_width,image_height = img.size
        #     img = img.convert("RGBA")
        #     img_data = bytes(img.tobytes())
        #     glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,image_width,image_height,0,GL_RGBA,GL_UNSIGNED_BYTE,img_data)
        # glGenerateMipmap(GL_TEXTURE_2D)
    
    def get_bounding_box(self, letter):
        if letter in self.letterTexCoords:
            return self.letterTexCoords[letter]
        return None
    
    # Top left - top right - bottom right - bottom left
    def get_text_coord(self, letter):
        if letter in self.letterTexCoords:
            top_left = (self.letterTexCoords[letter][0] + self.letterTexCoords[letter][2], self.letterTexCoords[letter][1] + self.letterTexCoords[letter][3])
            top_right = (self.letterTexCoords[letter][0] - self.letterTexCoords[letter][2], self.letterTexCoords[letter][1] + self.letterTexCoords[letter][3])
            bottom_right = (self.letterTexCoords[letter][0] - self.letterTexCoords[letter][2], self.letterTexCoords[letter][1] - self.letterTexCoords[letter][3])
            bottom_left = (self.letterTexCoords[letter][0] + self.letterTexCoords[letter][2], self.letterTexCoords[letter][1] - self.letterTexCoords[letter][3])
            return (top_left, top_right, bottom_right, bottom_left)
        return None
    
    def use(self):
        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D,self.texture)

    def destroy(self):
        glDeleteTextures(1, (self.texture,))

class Camera:
    def __init__(self):
        self.pos = np.array([0.0, 0.0, 10.0])
        # self.pos = np.array([0.0, 20.0, -10.0])
        self.front = np.array([0.0, 0.0, -1.0])
        self.up = np.array([0.0, 1.0, 0.0])
        self.speed = 0.1
        self.right = np.cross(self.front, self.up)
        self.sensitivity = 0.1
        self.yaw = -90.0
        self.pitch = 0.0
        self.yawShake = 0
        self.pitchShake = 0
        self.pitchCycle = itertools.cycle(list(range(-40, 41)) + list(range(40, -41, -1)))
        self.yawCycle = itertools.cycle(list(range(-60, 61)) + list(range(60, -61, -1)))
        self.minY = -20.0
        self.ySpeed = 0.0
        self.g = 0.2
        self.tick = 60
        self.enableGravity = True
        self.reset_position = np.array([0.0, 0.0, 10.0])
        self.canJump = False

        addToObjs((-1000.0, self.minY, -1000.0), (1000.0, self.minY, 1000.0))

    def process_mouse_movement(self, xoffset, yoffset):
        xoffset *= self.sensitivity
        yoffset *= self.sensitivity

        self.yaw += xoffset
        self.pitch -= yoffset

        if self.pitch > 89.0:
            self.pitch = 89.0
        if self.pitch < -89.0:
            self.pitch = -89.0

        self.update_camera_vectors()

    def update_camera_vectors(self):
        front = np.array([
            np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
            np.sin(np.radians(self.pitch)),
            np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))
        ])
        self.front = front / np.linalg.norm(front)
        self.right = np.cross(self.front, self.up)
        self.right /= np.linalg.norm(self.right)

    def process_input(self):

        keys = pygame.key.get_pressed()
        potential_pos = self.pos.copy()

        if keys[K_LSHIFT]:
            self.speed = 0.13
        else:
            self.speed = 0.05

        # Jump
        if keys[K_SPACE] and self.canJump:
            sound.play_jump_sfx()
            self.ySpeed = -0.080

        # Movement
        movement_keys_pressed = keys[K_w] or keys[K_a] or keys[K_s] or keys[K_d]

        if movement_keys_pressed and not keys[K_SPACE]:
            sound.play_footstep_sfx()
        else:
            sound.stop_footstep_sfx()

        if keys[K_w]:
            if self.enableGravity:
                potential_pos += self.speed * np.array([self.front[0], 0.0, self.front[2]])
            else:
                potential_pos += self.speed * self.front

        if keys[K_s]:
            if self.enableGravity:
                potential_pos -= self.speed * np.array([self.front[0], 0.0, self.front[2]])
            else:
                potential_pos -= self.speed * self.front

        if keys[K_a]:
            potential_pos -= self.speed * self.right

        if keys[K_d]:
            potential_pos += self.speed * self.right

        if (isinstance(self.check_collision(potential_pos, objects_for_collision), np.ndarray)):
            self.pos = self.check_collision(potential_pos, objects_for_collision)

    def update_view(self):
        self.shake()
        if (self.enableGravity):
            self.gravity()
        look_at = self.pos + self.front
        gluLookAt(self.pos[0], self.pos[1], self.pos[2],
                  look_at[0], look_at[1], look_at[2],
                  self.up[0], self.up[1], self.up[2])

    def check_collision(self, potential_pos, objects):
        # Basit bir AABB çarpışma kontrolü
        new_pos = potential_pos
        for obj in objects_for_collision:
            v1, v2 = obj
            xColliding = min(v1[0], v2[0]) - 0.1 <= potential_pos[0] <= max(v1[0], v2[0]) + 0.1 or (
                        v1[0] == v2[0] and min(self.pos[0], potential_pos[0]) - 0.1 <= v1[0] <= max(self.pos[0],
                                                                                                    potential_pos[
                                                                                                        0]) + 0.1)
            yColliding = min(v1[1], v2[1]) - 0.1 <= potential_pos[1] <= max(v1[1], v2[1]) + 1.2 or (
                        v1[1] == v2[1] and min(self.pos[1], potential_pos[1]) - 0.1 <= v1[1] <= max(self.pos[1],
                                                                                                    potential_pos[
                                                                                                        1]) + 1.2)
            zColliding = min(v1[2], v2[2]) - 0.1 <= potential_pos[2] <= max(v1[2], v2[2]) + 0.1 or (
                        v1[2] == v2[2] and min(self.pos[2], potential_pos[2]) - 0.1 <= v1[2] <= max(self.pos[2],
                                                                                                    potential_pos[
                                                                                                        2]) + 0.1)
            if (xColliding and yColliding and zColliding):
                new_pos[0] = self.check_collision1d([potential_pos[0], self.pos[1], self.pos[2]], objects_for_collision)[0]
                new_pos[1] = self.check_collision1d([self.pos[0], potential_pos[1], self.pos[2]], objects_for_collision)[1]
                new_pos[2] = self.check_collision1d([self.pos[0], self.pos[1], potential_pos[2]], objects_for_collision)[2]
                
        for obj in obstacles_for_collision:
            v1, v2 = obj
            xColliding = min(v1[0], v2[0]) - 0.1 <= potential_pos[0] <= max(v1[0], v2[0]) + 0.1 or (
                        v1[0] == v2[0] and min(self.pos[0], potential_pos[0]) - 0.1 <= v1[0] <= max(self.pos[0],
                                                                                                    potential_pos[
                                                                                                        0]) + 0.1)
            yColliding = min(v1[1], v2[1]) - 0.1 <= potential_pos[1] <= max(v1[1], v2[1]) + 1.2 or (
                        v1[1] == v2[1] and min(self.pos[1], potential_pos[1]) - 0.1 <= v1[1] <= max(self.pos[1],
                                                                                                    potential_pos[
                                                                                                        1]) + 1.2)
            zColliding = min(v1[2], v2[2]) - 0.1 <= potential_pos[2] <= max(v1[2], v2[2]) + 0.1 or (
                        v1[2] == v2[2] and min(self.pos[2], potential_pos[2]) - 0.1 <= v1[2] <= max(self.pos[2],
                                                                                                    potential_pos[
                                                                                                        2]) + 0.1)
            if (xColliding and yColliding and zColliding):
                self.pos = self.reset_position
        return new_pos

    def check_collision1d(self, potential_pos, objects):
        # Basit bir AABB çarpışma kontrolü
        new_pos = potential_pos
        for obj in objects:
            v1, v2 = obj
            xColliding = min(v1[0], v2[0]) - 0.1 <= potential_pos[0] <= max(v1[0], v2[0]) + 0.1 or (
                        v1[0] == v2[0] and min(self.pos[0], potential_pos[0]) - 0.1 <= v1[0] <= max(self.pos[0],
                                                                                                    potential_pos[
                                                                                                        0]) + 0.1)
            yColliding = min(v1[1], v2[1]) - 0.1 <= potential_pos[1] <= max(v1[1], v2[1]) + 1.2 or (
                        v1[1] == v2[1] and min(self.pos[1], potential_pos[1]) - 0.1 <= v1[1] <= max(self.pos[1],
                                                                                                    potential_pos[
                                                                                                        1]) + 1.2)
            zColliding = min(v1[2], v2[2]) - 0.1 <= potential_pos[2] <= max(v1[2], v2[2]) + 0.1 or (
                        v1[2] == v2[2] and min(self.pos[2], potential_pos[2]) - 0.1 <= v1[2] <= max(self.pos[2],
                                                                                                    potential_pos[
                                                                                                        2]) + 0.1)
            if (xColliding and yColliding and zColliding):
                new_pos = self.pos
        return new_pos

    def shake(self):
        front = np.array([
            np.cos(np.radians(self.yaw + self.yawShake)) * np.cos(np.radians(self.pitch + self.pitchShake)),
            np.sin(np.radians(self.pitch + self.pitchShake)),
            np.sin(np.radians(self.yaw + self.yawShake)) * np.cos(np.radians(self.pitch + self.pitchShake))
        ])
        self.front = front / np.linalg.norm(front)
        self.right = np.cross(self.front, self.up)
        self.right /= np.linalg.norm(self.right)

        self.yawShake = next(self.yawCycle) / 200
        self.pitchShake = next(self.pitchCycle) / 120

    def gravity(self):
        new_y = self.pos[1] - self.ySpeed
        self.ySpeed += self.g / self.tick
        new_pos = [self.pos[0], new_y, self.pos[2]]
        if (new_pos[1] != self.check_collision(new_pos, objects_for_collision)[1]):
            if self.pos[1] >= new_y:
                self.canJump = True
            self.ySpeed = 0.0
            return
        self.canJump = False
        self.pos = new_pos

def drawWall3d(v1, v2, texture, isObstacle = False):
    vertices = []
    x = (v1[0], v2[0])
    y = (v1[1], v2[1])
    z = (v1[2], v2[2])
    width = abs(v1[0] - v2[0])
    height = abs(v1[1] - v2[1])
    depth = abs(v1[2] - v2[2])
    for vertice in itertools.product(x, y, z):
        vertices.append(vertice)

    faces = [
        (0, 1, 3, 2, (0.0, 0.0), (depth / 3, 0.0), (depth / 3, height / 3), (0.0, height / 3)),  # depth, heigth
        (4, 5, 7, 6, (0.0, 0.0), (depth / 3, 0.0), (depth / 3, height / 3), (0.0, height / 3)),  # depth, height
        (0, 1, 5, 4, (0.0, 0.0), (depth / 3, 0.0), (depth / 3, width / 3), (0.0, width / 3)),  # depth, width
        (2, 3, 7, 6, (0.0, 0.0), (depth / 3, 0.0), (depth / 3, width / 3), (0.0, width / 3)),  # depth, width
        (2, 6, 4, 0, (0.0, 0.0), (width / 3, 0.0), (width / 3, height / 3), (0.0, height / 3)),  # width, height
        (3, 7, 5, 1, (0.0, 0.0), (width / 3, 0.0), (width / 3, height / 3), (0.0, height / 3))  # width, height
    ]

    glBindTexture(GL_TEXTURE_2D, texture)
    glEnable(GL_TEXTURE_2D)
    glBegin(GL_QUADS)
    for face in faces:
        for i in range(4):
            glTexCoord2fv(face[i + 4])
            glVertex3fv(vertices[face[i]])
    glEnd()

    if not isObstacle:
        addToObjs(v1, v2)
    else:
        addToObstacles(v1, v2)

def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_DEPTH_CLAMP)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

def addToObjs(v1, v2):
    isThere = False
    for obj in objects_for_collision:
        if ((v1, v2) == obj):
            isThere = True
            break
    if not isThere:
        objects_for_collision.append((v1, v2))

def addToObstacles(v1, v2):
    isThere = False
    for obj in obstacles_for_collision:
        if ((v1, v2) == obj):
            isThere = True
            break
    if not isThere:
        obstacles_for_collision.append((v1, v2))

def load_texture(texture_file):
    texture_surface = pygame.image.load(texture_file).convert_alpha()
    texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)
    width = texture_surface.get_width()
    height = texture_surface.get_height()

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

    return texture_id

def drawLetter(start: tuple, size: tuple, letter):
    vertices = (
        start,
        (start[0], start[1], start[2] + size[0]),
        (start[0], start[1] - size[1], start[2] + size[0]),
        (start[0], start[1] - size[1], start[2])
    )
    

    text_coords = font.get_text_coord(letter)
    font.use()
    
    glBegin(GL_POLYGON)
    glColor3f(1.0, 1.0, 1.0)
    for i in range(4):
        glTexCoord2fv(text_coords[i])
        glVertex3fv(vertices[i])
    glEnd()

def drawText(start: tuple, size: tuple, text):
    for i, letter in enumerate(text):
        drawLetter((start[0], start[1], start[2] - i), size, letter)

def main():
    global font
    pygame.init()
    pygame.mixer.init()
    ctypes.windll.user32.SetProcessDPIAware()

    display = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL | pygame.FULLSCREEN)

    init()
    sound.init()
    skybox.init()
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    elapsed_time = 0
    finished = False

    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, (display[0] / display[1]), 0.1, 200.0)
    cam = Camera()
    glMatrixMode(GL_MODELVIEW)

    # Load Textures
    ground_texture_id = load_texture("texture/ground.jpg")
    wall_texture_id = load_texture("texture/lab_2.jpg")
    parkour_texture_id = load_texture("texture/texture 4.jpg")
    obstacle_texture_id = load_texture("texture/texture 7.jpg")
    font = Font()

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                font.destroy()
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                cam.enableGravity = not cam.enableGravity

        cam.process_input()
        xoffset, yoffset = pygame.mouse.get_rel()
        cam.process_mouse_movement(xoffset, yoffset)
        cur_pos = pygame.mouse.get_pos()
        if not (0 < cur_pos[0] < display[0] - 1 and 0 < cur_pos[1] < display[1] - 1):
            pygame.mouse.set_pos(display[0] // 2, display[1] // 2)
        pygame.mouse.set_visible(False)

        glViewport(0, 0, display[0], display[1])
        
        
        glLoadIdentity()
        cam.update_view()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # drawWall3d((-10.0, 0.0, 20.0), (0.0, 10.0, 30.0), font_text)
        glColor3f(1.0, 1.0, 1.0)
        # Draw skybox
        skybox.draw_skybox(skybox_size=100)

        # Timer
        if not (11.1 > cam.pos[0] > -13.6) or not(13.1 > cam.pos[2] > -19.6):
            finished = True
        if not finished:
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        minute = elapsed_time // 60
        seconds = elapsed_time % 60
        drawText((-30.0, 10.0, 0.0), (1, 1), f"Zaman:{minute}.{seconds:02}")

        # glColor3f(0.1, 0.1, 0.1) # Make darker
        
        # Draw ground
        drawWall3d((-50, -2, -50), (50, -3, 50), ground_texture_id)

        # İlk kat
        drawWall3d((2, 2, 5), (1.5, -2, 1.5), wall_texture_id)
        drawWall3d((2, 2, 1.5), (-1.5, -2, 2), wall_texture_id)
        drawWall3d((-1.5, 2, 2), (-1, -2, -1), wall_texture_id)
        drawWall3d((-13.5, 2, 5), (-1, -2, 4.5), wall_texture_id)
        drawWall3d((-4.5, 2, 5), (-4, -2, 1.5), wall_texture_id)
        drawWall3d((-4, 2, 2), (-10.5, -2, 1.5), wall_texture_id)
        drawWall3d((5, 2, -1), (-7.5, -2, -1.5), wall_texture_id)
        drawWall3d((-4, 2, -1), (-4.5, -2, -4.5), wall_texture_id)
        drawWall3d((-10, 2, 2), (-10.5, -2, -4.5), wall_texture_id)
        drawWall3d((-7, 2, -4), (-10.5, -2, -4.5), wall_texture_id)
        drawWall3d((-7.5, 2, -4), (-7, -2, -7.5), wall_texture_id)
        drawWall3d((-1, 2, -7), (-10.5, -2, -7.5), wall_texture_id)
        drawWall3d((-1, 2, -4), (-1.5, -2, -7.5), wall_texture_id)
        drawWall3d((5, 2, -4), (-1.5, -2, -4.5), wall_texture_id)
        drawWall3d((5, 2, -4), (4.5, -2, -7.5), wall_texture_id)
        drawWall3d((8, 2, -7), (1.5, -2, -7.5), wall_texture_id)
        drawWall3d((2, 2, -7), (1.5, -2, -10.5), wall_texture_id)
        drawWall3d((8, 2, -7), (7.5, -2, -10.5), wall_texture_id)
        drawWall3d((11, 2, -13), (-1.5, -2, -13.5), wall_texture_id)
        drawWall3d((5, 2, -10), (4.5, -2, -13.5), wall_texture_id)
        drawWall3d((8, 2, -13), (7.5, -2, -16.5), wall_texture_id)
        drawWall3d((11, 2, 5), (10.5, -2, -19.5), wall_texture_id)
        # drawWall3d((11, 2, -19), (-1.5, -2, -19.5), wall_texture_id)
        # drawWall3d((-4, 2, -19), (-13.5, -2, -19.5), wall_texture_id)
        drawWall3d((11, 2, -19), (-13.5, -2, -19.5), wall_texture_id)
        drawWall3d((5, 2, -16), (4.5, -2, -19.5), wall_texture_id)
        drawWall3d((4.5, 2, 2), (8, -2, 1.5), wall_texture_id)
        drawWall3d((5, 2, 2), (4.5, -2, -1.5), wall_texture_id)
        drawWall3d((8, 2, -1), (7.5, -2, -4.5), wall_texture_id)
        drawWall3d((11, 2, -1), (7.5, -2, -1.5), wall_texture_id)
        drawWall3d((11, 2, 5), (1.5, -2, 4.5), wall_texture_id)
        drawWall3d((-13, 2, 5), (-13.5, -2, -19.5), wall_texture_id)
        drawWall3d((-10, 2, -10), (-13.5, -2, -10.5), wall_texture_id)
        drawWall3d((-10, 2, -16), (-13.5, -2, -16.5), wall_texture_id)
        drawWall3d((-4, 2, -13), (-4.5, -2, -19.5), wall_texture_id)
        drawWall3d((2, 2, -16), (-4.5, -2, -16.5), wall_texture_id)
        drawWall3d((-7, 2, -13), (-10.5, -2, -13.5), wall_texture_id)
        drawWall3d((-7, 2, -10), (-7.5, -2, -16.5), wall_texture_id)
        drawWall3d((-1, 2, -10), (-7.5, -2, -10.5), wall_texture_id)
        drawWall3d((-1, 2, -10), (-1.5, -2, -13.5), wall_texture_id)
        drawWall3d((-1, -1.5, 4.5), (-1.5, -2, 2), obstacle_texture_id, True)
        drawWall3d((-4, -1.5, 1.5), (-4.5, -2, -1), obstacle_texture_id, True)
        drawWall3d((4.5, -1.5, -10), (1.5, -2, -10.5), obstacle_texture_id, True)
        drawWall3d((-10.5, -1.5, -7), (-13, -2, -7.5), obstacle_texture_id, True)
        drawWall3d((5, -1.5, -13.5), (4.5, -2, -16), obstacle_texture_id, True)
        drawWall3d((-1.5, -1.5, -13), (-4, -2, -13.5), obstacle_texture_id, True)
        
        
        # Başlangıç
        drawWall3d((-1, 2, 5), (-1.5, -2, 13), wall_texture_id)
        drawWall3d((1.5, 2, 5), (2.0, -2, 13), wall_texture_id)
        drawWall3d((-1.0, 2, 12.5), (1.5, -2, 13), wall_texture_id)
        
        # Merdiven
        drawWall3d((4.0, -1.2, -19.0), (4.5, -1.5, -17.0), parkour_texture_id)
        drawWall3d((-1.0, -0.2, -19.0), (1.5, -0.5, -18.5), parkour_texture_id)
        drawWall3d((-3.5, 0.8, -19.0), (-4.0, 0.5, -17.0), parkour_texture_id)
        drawWall3d((-1.5, 1.8, -17.0), (-3.5, 1.5, -16.5), parkour_texture_id)
        drawWall3d((-2.5, 2, -17.0), (-3.5, 1.8, -16.5), parkour_texture_id)
        
        # İkinci kat
        # Yer        
        drawWall3d((-50.0, 2, -16.5), (50.0, 3, 50), ground_texture_id)
        drawWall3d((-50.0, 2, -16.5), (-4.0, 3, -50.0), ground_texture_id)
        drawWall3d((50.0, 2, -16.5), (-1.5, 3, -50.0), ground_texture_id)
        drawWall3d((-1.5, 2, -19.0), (-4.0, 3, -50), ground_texture_id)
        
        # Yan duvarlar
        drawWall3d((-13.5, 3.0, 5.0), (-13.0, 7.0, -2.5), wall_texture_id)
        drawWall3d((-13.5, 3.0, -5.5), (-13.0, 7.0, -19.5), wall_texture_id)
        drawWall3d((11.0, 3.0, 5.0), (10.5, 7.0, -19.5), wall_texture_id)
        drawWall3d((-13.5, 3.0, 5.0), (11.0, 7.0, 4.5), wall_texture_id)
        drawWall3d((-13.5, 3.0, -19.5), (11.0, 7.0, -19.0), wall_texture_id)
        
        # İç duvarlar
        drawWall3d((-4.5, 3, -19.0), (-4.0, 7, -13.0), wall_texture_id)
        drawWall3d((-1.0, 3, -13.0), (-6.0, 7, -12.5), wall_texture_id)
        drawWall3d((-1.5, 3, -13.0), (-1.0, 7, -9.0), wall_texture_id)
        
        drawWall3d((3.0, 3, -9.0), (-1.5, 7, -8.5), wall_texture_id)
        drawWall3d((0.5, 3, -8.5), (1.0, 7, 2.0), wall_texture_id)
        drawWall3d((-1.5, 3, 2.0), (1.0, 7, 1.5), wall_texture_id)
        
        drawWall3d((5.5, 3, -6.0), (1.0, 7, -5.5), wall_texture_id)
        drawWall3d((5.5, 3, -13.0), (5.0, 7, 2.0), wall_texture_id)
        drawWall3d((8.5, 3, 2.0), (5.0, 7, 1.5), wall_texture_id)
        drawWall3d((8.5, 3, -3.5), (8.0, 7, 2.0), wall_texture_id)
        drawWall3d((3.25, 3, -3.5), (2.75, 7, 5.0), wall_texture_id)
        
        drawWall3d((-1.5, 3, -19.0), (-1.0, 7, -16.5), wall_texture_id)
        drawWall3d((-1.5, 3, -16.0), (1.0, 7, -16.5), wall_texture_id)
        drawWall3d((0.5, 3, -16.5), (1.0, 7, -13.0), wall_texture_id)

        drawWall3d((-7.5, 3, -19.0), (-8.0, 7, -8.0), wall_texture_id)
        drawWall3d((-11.5, 3, -16.0), (-5.5, 7, -15.5), wall_texture_id)
        drawWall3d((-3.0, 3, -8.0), (-7.5, 7, -8.5), wall_texture_id)
        drawWall3d((-3.0, 3, -8.0), (-3.5, 7, -5.5), wall_texture_id)
        drawWall3d((-1.0, 3, -5.0), (-3.5, 7, -5.5), wall_texture_id)
        drawWall3d((-1.0, 3, -2.0), (-1.5, 7, -5.5), wall_texture_id)
        drawWall3d((-1.0, 3, -2.0), (-3.5, 7, -2.5), wall_texture_id)
        drawWall3d((-3.0, 3, -2.0), (-3.5, 7, 2.0), wall_texture_id)
        
        drawWall3d((-5.0, 3, -5.5), (-5.5, 7, 5.0), wall_texture_id)
        drawWall3d((-5.0, 3, -5.0), (-9.5, 7, -5.5), wall_texture_id)
        drawWall3d((-10.0, 3, -12.5), (-9.5, 7, -1.0), wall_texture_id)
        drawWall3d((-10.0, 3, -12.5), (-11.5, 7, -12.0), wall_texture_id)
        drawWall3d((-11.5, 3, -12.0), (-11.0, 7, -8.0), wall_texture_id)
        drawWall3d((-7.0, 3, -1.0), (-9.5, 7, -1.5), wall_texture_id)
        drawWall3d((-7.0, 3, -1.0), (-7.5, 7, 2.0), wall_texture_id)

        drawWall3d((-13.5, 3, -5.5), (-11.0, 7, -5.0), wall_texture_id)
        drawWall3d((-11.0, 3, -5.0), (-11.5, 7, 2.0), wall_texture_id)
        drawWall3d((-11.5, 3, 2.5), (-9.0, 7, 2.0), wall_texture_id)

        drawWall3d((3.0, 3, -19.0), (2.5, 7, -11.0), wall_texture_id)

        drawWall3d((11.0, 3, -6.0), (8.5, 7, -6.5), wall_texture_id)
        drawWall3d((8.5, 3, -16.5), (8.0, 7, -6.0), wall_texture_id)
        drawWall3d((8.5, 3, -16.0), (6.0, 7, -16.5), wall_texture_id)
        
        
        
        
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()