import glfw, numpy, pyrr
from OpenGL.GL import *
import OpenGL.GL.shaders
from PIL import Image


def main():
    if not glfw.init():
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    window = glfw.create_window(800,600,"My OpenGL Window", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

#                Verts       Colors         Texture
    quad = [-0.5, -0.5, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0,
             0.5, -0.5, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0,
             0.5,  0.5, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 
            -0.5,  0.5, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0]

    quad = numpy.array(quad, dtype = numpy.float32)

    indicies = [0, 1, 2,
                2, 3, 0]

    print(quad.itemsize * len(quad))
    print(indicies.itemsize * len(indicies))
    print(quad.itemsize * 8)

    indicies = numpy.array(indicies, dtype = numpy.uint32)

    vertex_shader = """
    #version 410 core
    in vec3 position;
    in vec3 color;
    in vec2 inTexCoords;

    out vec3 newcolor;
    out vec2 outTexCoords;

    void main()
    {
        gl_Position = vec4(position, 1.0f);
        newcolor = color;
        outTexCoords = inTexCoords;
    }

    """

    fragment_shader = """
    #version 410 core
    in vec3 newcolor;
    in vec2 outTexCoords;
    
    out vec4 outcolor;
    uniform sampler2D samplerTex;
    void main()
    {
        outcolor = texture(samplerTex, outTexCoords);
    }
    """

    glfw.make_context_current(window)

    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)
    
    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(fragment_shader,GL_FRAGMENT_SHADER))

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, quad.itemsize * len(quad), quad, GL_STATIC_DRAW)

    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indicies.itemsize * len(indicies), indicies, GL_STATIC_DRAW)

    position = glGetAttribLocation(shader, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, quad.itemsize * 8, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)

    color = glGetAttribLocation(shader, "color")
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, quad.itemsize * 8, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)

    texture_coords = glGetAttribLocation(shader, "inTexCoords")
    glVertexAttribPointer(texture_coords, 2, GL_FLOAT, GL_FALSE, quad.itemsize * 8, ctypes.c_void_p(24))
    glEnableVertexAttribArray(texture_coords)

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    image = Image.open("crate.jpg")
    img_data = numpy.array(list(image.getdata()), numpy.uint8)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    glGenerateMipmap(GL_TEXTURE_2D)
    

    glUseProgram(shader)

    
    glClearColor(0.2, 0.3, 0.2, 1.0)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT)

        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
