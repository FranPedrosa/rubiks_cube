from numpy import random

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math

import magic_cube
import keys

glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
window = glfw.create_window(700, 700, "Cubo", None, None)
glfw.make_context_current(window)

vertex_code = """
        attribute vec3 position;
        uniform mat4 mat_transformation;
        void main(){
            gl_Position = mat_transformation * vec4(position,1.0);
        }
        """
fragment_code = """
        uniform vec4 color;
        void main(){
            gl_FragColor = color;
        }
        """
program = glCreateProgram()
vertex = glCreateShader(GL_VERTEX_SHADER)
fragment = glCreateShader(GL_FRAGMENT_SHADER)
glShaderSource(vertex, vertex_code)
glShaderSource(fragment, fragment_code)
glCompileShader(vertex)
if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(vertex).decode()
    print(error)
    raise RuntimeError("Erro de compilacao do Vertex Shader")
glCompileShader(fragment)
if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(fragment).decode()
    print(error)
    raise RuntimeError("Erro de compilacao do Fragment Shader")
glAttachShader(program, vertex)
glAttachShader(program, fragment)
glLinkProgram(program)
if not glGetProgramiv(program, GL_LINK_STATUS):
    print(glGetProgramInfoLog(program))
    raise RuntimeError('Linking error')

glUseProgram(program)


vertices = np.zeros(magic_cube.num_points, [("position", np.float32, 3)])
vertices['position'] = magic_cube.generate()

buffer = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER,buffer)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)
glBindBuffer(GL_ARRAY_BUFFER,buffer)
loc = glGetAttribLocation(program, "position")
stride = vertices.strides[0]
offset = ctypes.c_void_p(0)
glEnableVertexAttribArray(loc)
glVertexAttribPointer(0, 3, GL_FLOAT, False, stride,offset)


def matrix_multiplication(a, b):
    m_a = a.reshape(4, 4)
    m_b = b.reshape(4, 4)
    m_c = np.dot(m_a, m_b)
    c = m_c.reshape(1, 16)
    return c

def rotate_x(d):
    cos_d = math.cos(d)
    sin_d = math.sin(d)
    return np.array([  1.0,   0.0,    0.0, 0.0,
                       0.0, cos_d, -sin_d, 0.0,
                       0.0, sin_d,  cos_d, 0.0,
                       0.0,   0.0,    0.0, 1.0], np.float32)

def rotate_y(d):
    cos_d = math.cos(d)
    sin_d = math.sin(d)
    return np.array([      cos_d,  0.0, sin_d, 0.0,
                          0.0,  1.0,   0.0, 0.0,
                       -sin_d,  0.0, cos_d, 0.0,
                          0.0,  0.0,   0.0, 1.0], np.float32)

def rotate_z(d):
    cos_d = math.cos(d)
    sin_d = math.sin(d)
    return np.array([  cos_d, -sin_d, 0.0, 0.0,
                       sin_d,  cos_d, 0.0, 0.0,
                       0.0  ,    0.0, 1.0, 0.0,
                       0.0  ,    0.0, 0.0, 1.0], np.float32)

def scale_transformation():
    return np.array([scale_p, 0, 0, 0,
                    0, scale_p, 0, 0,
                    0, 0, scale_p, 0,
                    0, 0, 0, 1], np.float32)

def translation_transformation():
    return np.array([1, 0, 0, t_x,
                    0, 1, 0, t_y,
                    0, 0, 1, t_z,
                    0, 0, 0, 1], np.float32)

#Rotação do cubo
a_x = 0.0
a_y = 0.0
a_z = 0.0

#?
anim_x = 0.0
anim_y = 0.0
anim_z = 0.0

#?
d_x = 0.0
d_y = 0.0
d_z = 0.0

#escala da figura
scale_p = 1.0

#translation
t_x = 0.0
t_y = 0.0
t_z = 0.0

calback = None

def increment_animation():
    global anim_x
    global anim_y
    global anim_z
    anim_x += d_x
    anim_y += d_y
    anim_z += d_z
    if anim_x > math.pi/2 or anim_y > math.pi/2 or anim_z > math.pi/2:
        magic_cube.animation = False
        anim_x = 0.0
        anim_y = 0.0
        anim_z = 0.0
        magic_cube.moving = []
        callback()
        

def key_event(window, key, scancode, action, mods):
    global a_x, a_y, a_z
    global d_x
    global scale_p, t_x, t_y
    global callback
    print(key)
    if action == 1 or action == 2:
        if key == keys.up:
            a_x -= 0.1
        if key == keys.down:
            a_x += 0.1
        if key == keys.left:
            a_y += 0.1
        if key == keys.right:
            a_y -= 0.1
        if key == keys.t_up:
            t_y += 0.1
        if key == keys.t_down:
            t_y -= 0.1
        if key == keys.t_right:
            t_x += 0.1
        if key == keys.t_left:
            t_x -= 0.1
        if key == keys.scale_plus:
            scale_p += 0.1
        if key == keys.scale_minus:
            scale_p -= 0.1
        if key == keys.r:
            d_x = 0.01
            callback = magic_cube.move_white()


glfw.set_key_callback(window, key_event)
loc_color = glGetUniformLocation(program, "color")
glfw.show_window(window)
glEnable(GL_DEPTH_TEST)


while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.5, 0.5, 0.5, 1.0)



    loc = glGetUniformLocation(program, "mat_transformation")
    mat_transform = rotate_x(a_x)
    mat_transform = matrix_multiplication(rotate_y(a_y),mat_transform)
    mat_transform = matrix_multiplication(rotate_z(a_z),mat_transform)
    mat_transform = matrix_multiplication(translation_transformation(),mat_transform)
    mat_transform = matrix_multiplication(scale_transformation(),mat_transform)
    glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transform)
    j =0
    i =0

    for cube in range(magic_cube.num_cubes):
        for c in magic_cube.cube_colors[i]:
            if not cube in magic_cube.moving:
                glUniform4f(loc_color, c['r'], c['g'], c['b'], 1.0)
                glDrawArrays(GL_TRIANGLE_STRIP, j*4, 4)
            j += 1
        i+= 1

    if magic_cube.animation:
        print(magic_cube.moving)
        j =0
        i =0
        mat_anim = rotate_x(anim_x)
        mat_anim = matrix_multiplication(rotate_y(anim_y),mat_transform)
        mat_anim = matrix_multiplication(rotate_z(anim_z),mat_transform)
        mat_transform = matrix_multiplication(scale_transformation(),mat_transform)
        glUniformMatrix4fv(loc, 1, GL_TRUE, mat_anim)
        for cube in range(magic_cube.num_cubes):
            for c in magic_cube.cube_colors[i]:
                if cube in magic_cube.moving:
                    glUniform4f(loc_color, c['r'], c['g'], c['b'], 1.0)
                    glDrawArrays(GL_TRIANGLE_STRIP, j*4, 4)
                j += 1
            i += 1
        increment_animation()

    glfw.swap_buffers(window)
glfw.terminate()
