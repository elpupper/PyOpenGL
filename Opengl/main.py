import glfw, numpy, pyrr
from pyrr import matrix44, Vector3, Matrix44
from OpenGL.GL import *
import ShaderLoader
from PIL import Image
from OBJLoader import *
from camera import Camera
from math import sin,cos
import TextureLoader
import os


keys = [False] * 1024
cam = Camera()
lastX, lastY = 720, 450
first_mouse = True
filename = "Screenshot_1.jpg"

mouse_x,mouse_y = 0,0

def render_to_jpg(format="JPEG"):
    global filename
    os.chdir(r"/Users/Datboi/Desktop/OGL/Screenshots")
    for file in os.listdir(os.curdir):
        if file == filename:
            name, ext = file.split(".")
            word, number = name.split("_")
            new_num = int(number) + 1
            filename = word + "_" + str(new_num) + "." + ext
        else:
            continue
        
    x,y,width,height = glGetDoublev(GL_VIEWPORT)
    width,height = int(width), int(height)
    glPixelStorei(GL_PACK_ALIGNMENT,1)
    data = glReadPixels(x,y,width,height,GL_RGB,GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGB",(width,height),data)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image.save(filename, format)

def key_callback(window, key, scancode, action, mode):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)
    if key == glfw.KEY_F12 and action == glfw.PRESS:
        render_to_jpg()

    if key >= 0 and key < 1024:
        if action == glfw.PRESS:
            keys[key] = True
        elif action == glfw.RELEASE:
            keys[key] = False

def do_movement():
    if keys[glfw.KEY_W]:
        cam.process_keyboard("FORWARD", 0.1)
    if keys[glfw.KEY_S]:
        cam.process_keyboard("BACKWARD", 0.1)
    if keys[glfw.KEY_A]:
        cam.process_keyboard("LEFT", 0.1)
    if keys[glfw.KEY_D]:
        cam.process_keyboard("RIGHT", 0.1)

def cursor_pos_callback(window, xpos, ypos):
    global mouse_x, mouse_y
    width,height = glfw.get_window_size(window)
    mouse_x = xpos
    mouse_y = height - ypos

def mouse_button_callback(window,button,action,mods):
    data = glReadPixels(mouse_x, mouse_y, 1, 1, GL_RGB, GL_FLOAT)

def mouse_callback(window, xpos, ypos):
    global first_mouse,lastX, lastY
    if first_mouse:
        lastX = xpos
        lastY = ypos
        first_mouse = False
        
    xoffset = xpos - lastX
    yoffset = lastY - ypos

    lastX = xpos
    lastY = ypos

    cam.process_mouse_movement(xoffset, yoffset)

print(glfw.KEY_W)
    
def main():
    if not glfw.init():
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    w_width, w_height = 1440,900
    
    window = glfw.create_window(w_width,w_height,"My OpenGL Window", None, None)
    #window = glfw.create_window(w_width,w_height,"My OpenGL Window", glfw.get_primary_monitor(), None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, mouse_callback)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    monkey_obj = ObjLoader()
    monkey_obj.load_model('monkey.obj')
    monkey_tex = TextureLoader.load_texture("res/monkey.png")
    monkey_tex_offset = len(monkey_obj.vertex_index)*12
    monkey_norm_offset = (monkey_tex_offset + len(monkey_obj.texture_index) * 8)

    sphere_obj = ObjLoader()
    sphere_obj.load_model('sphere2.obj')
    sphere_tex = TextureLoader.load_texture("res/yellow.png")
    sphere_tex_offset = len(sphere_obj.vertex_index)*12
    sphere_norm_offset = (sphere_tex_offset + len(sphere_obj.texture_index) * 8)

    shader = ShaderLoader.compile_shader("Shaders/vert.vs", "Shaders/frag.fs")

    sphere_vao = glGenVertexArrays(1)
    glBindVertexArray(sphere_vao)
    sphere_VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, sphere_VBO)
    glBufferData(GL_ARRAY_BUFFER, sphere_obj.model.itemsize * len(sphere_obj.model), sphere_obj.model, GL_STATIC_DRAW)
    #Position
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sphere_obj.model.itemsize * 3, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    #TextureCoords
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, sphere_obj.model.itemsize * 2, ctypes.c_void_p(sphere_tex_offset))
    glEnableVertexAttribArray(1)
    #Normals
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, sphere_obj.model.itemsize * 3, ctypes.c_void_p(sphere_norm_offset))
    glEnableVertexAttribArray(2)
    glBindVertexArray(0)

    monkey_vao = glGenVertexArrays(1)
    glBindVertexArray(monkey_vao)
    monkey_VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, monkey_VBO)
    glBufferData(GL_ARRAY_BUFFER, monkey_obj.model.itemsize * len(monkey_obj.model), monkey_obj.model, GL_STATIC_DRAW)
    #Position
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, monkey_obj.model.itemsize * 3, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    #TextureCoords
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, monkey_obj.model.itemsize * 2, ctypes.c_void_p(monkey_tex_offset))
    glEnableVertexAttribArray(1)
    #Normals
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, monkey_obj.model.itemsize * 3, ctypes.c_void_p(monkey_norm_offset))
    glEnableVertexAttribArray(2)
    glBindVertexArray(0)
    
    glClearColor(0.2, 0.3, 0.2, 1.0)
    glEnable(GL_DEPTH_TEST)
    

    projection = pyrr.matrix44.create_perspective_projection_matrix(60.0, w_width/w_height, 0.1, 100.0)
    sphere_model = matrix44.create_from_translation(Vector3([-4.0,0.0,-3.0]))
    monkey_model = matrix44.create_from_translation(Vector3([0.0,0.0,-3.0]))
    
    glUseProgram(shader)
    model_loc = glGetUniformLocation(shader, "model")
    view_loc = glGetUniformLocation(shader, "view")
    proj_loc = glGetUniformLocation(shader, "proj")
    light_loc = glGetUniformLocation(shader, "light")
    
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        do_movement()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        view = cam.get_view_matrix()
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

        light_y = Matrix44.from_y_rotation(0.5)
        rot_y = Matrix44.from_y_rotation(glfw.get_time() * 0.5)
        
        glUniformMatrix4fv(light_loc, 1, GL_FALSE, light_y)

        glBindVertexArray(sphere_vao)
        glBindTexture(GL_TEXTURE_2D, sphere_tex)
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, Matrix44(sphere_model) * rot_y)
        glDrawArrays(GL_TRIANGLES, 0, len(sphere_obj.vertex_index))
        glBindVertexArray(0)
        
        glBindVertexArray(monkey_vao)
        glBindTexture(GL_TEXTURE_2D, monkey_tex)
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, monkey_model)
        glDrawArrays(GL_TRIANGLES, 0, len(monkey_obj.vertex_index))
        glBindVertexArray(0)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
	main()
