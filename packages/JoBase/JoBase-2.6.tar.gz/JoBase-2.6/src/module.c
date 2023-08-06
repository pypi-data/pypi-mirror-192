#define _USE_MATH_DEFINES

#include <glad/glad.h>
#include <main.h>

#define READY(t) if(PyType_Ready(&t))return NULL;
#define BUILD(i, e) object=e;if(PyModule_AddObject(self,i,object)){Py_XDECREF(object);Py_DECREF(self);return -1;}
#define COLOR(i, r, g, b) BUILD(i,PyTuple_Pack(3,PyFloat_FromDouble(r),PyFloat_FromDouble(g),PyFloat_FromDouble(b)))
#define PATH(i, e) BUILD(i,PyUnicode_FromString(filepath(e)))

#define EXPAND(e) #e
#define STR(e) EXPAND(e)

#ifdef _WIN32
PyMODINIT_FUNC PyInit___init__;
#endif

static PyObject *Module_random(PyObject *Py_UNUSED(self), PyObject *args) {
    double x, y;

    if (!PyArg_ParseTuple(args, "dd", &x, &y)) return NULL;
    return PyFloat_FromDouble(rand() / (RAND_MAX / fabs(y - x)) + MIN(x, y));
}

static PyObject *Module_randint(PyObject *Py_UNUSED(self), PyObject *args) {
    int x, y;

    if (!PyArg_ParseTuple(args, "ii", &x, &y)) return NULL;
    return PyLong_FromLong(rand() / (RAND_MAX / abs(y - x + 1)) + MIN(x, y));
}

static PyObject *Module_sin(PyObject *Py_UNUSED(self), PyObject *value) {
    double angle = PyFloat_AsDouble(value);

    if (ERR(angle)) return NULL;
    return PyFloat_FromDouble(sin(angle));
}

static PyObject *Module_cos(PyObject *Py_UNUSED(self), PyObject *value) {
    double angle = PyFloat_AsDouble(value);

    if (ERR(angle)) return NULL;
    return PyFloat_FromDouble(cos(angle));
}

static PyObject *Module_tan(PyObject *Py_UNUSED(self), PyObject *value) {
    double angle = PyFloat_AsDouble(value);

    if (ERR(angle)) return NULL;
    return PyFloat_FromDouble(tan(angle));
}

static PyObject *Module_sqrt(PyObject *Py_UNUSED(self), PyObject *value) {
    double number = PyFloat_AsDouble(value);

    if (ERR(number)) return NULL;
    return PyFloat_FromDouble(sqrt(number));
}

static PyObject *Module_run(PyObject *Py_UNUSED(self), PyObject *Py_UNUSED(ignored)) {
    PyObject *module = PyDict_GetItemString(PySys_GetObject("modules"), "__main__");
    glfwShowWindow(window -> glfw);

    if (PyObject_HasAttrString(module, "loop") && !(loop = PyObject_GetAttrString(module, "loop")))
        return NULL;

    while (!glfwWindowShouldClose(window -> glfw)) {
        if (PyErr_CheckSignals() || PyErr_Occurred() || update()) return NULL;
        glfwPollEvents();
    }

    Py_RETURN_NONE;
}

static int Module_exec(PyObject *self) {
    if (!glfwInit()) {
        const char *buffer;
        glfwGetError(&buffer);

        PyErr_SetString(PyExc_OSError, buffer);
        Py_DECREF(self);
        return -1;
    }

    if (FT_Init_FreeType(&library)) {
        PyErr_SetString(PyExc_OSError, "failed to initialize FreeType");
        Py_DECREF(self);
        return -1;
    }

    Py_ssize_t size;
    PyObject *file = PyObject_GetAttrString(self, "__file__"), *object;

    if (!file) {
        Py_DECREF(self);
        return -1;
    }

    path = (char *) PyUnicode_AsUTF8AndSize(file, &size);
    Py_DECREF(file);

    if (!path) {
        Py_DECREF(self);
        return -1;
    }

    const char *last = strrchr(path, '/');
    length = size - strlen(last ? last : strrchr(path, '\\')) + 1;

    BUILD("cursor", PyObject_CallFunctionObjArgs((PyObject *) &CursorType, NULL))
    BUILD("key", PyObject_CallFunctionObjArgs((PyObject *) &KeyType, NULL))
    BUILD("camera", PyObject_CallFunctionObjArgs((PyObject *) &CameraType, NULL))
    BUILD("window", PyObject_CallFunctionObjArgs((PyObject *) &WindowType, NULL))

    BUILD("Rectangle", (PyObject *) &RectangleType)
    BUILD("Image", (PyObject *) &ImageType)
    BUILD("Text", (PyObject *) &TextType)
    BUILD("Circle", (PyObject *) &CircleType)
    BUILD("Line", (PyObject *) &LineType)
    BUILD("Shape", (PyObject *) &ShapeType)
    BUILD("Physics", (PyObject *) &PhysicsType)
    BUILD("Joint", (PyObject *) &JointType)
    BUILD("Pin", (PyObject *) &PinType)
    BUILD("Pivot", (PyObject *) &PivotType)
    BUILD("Motor", (PyObject *) &MotorType)
    BUILD("Spring", (PyObject *) &SpringType)
    BUILD("Groove", (PyObject *) &GrooveType)

    BUILD("DYNAMIC", PyLong_FromLong(CP_BODY_TYPE_DYNAMIC))
    BUILD("STATIC", PyLong_FromLong(CP_BODY_TYPE_KINEMATIC))
    BUILD("PI", PyFloat_FromDouble(M_PI))

    PATH("MAN", "images/man.png")
    PATH("COIN", "images/coin.png")
    PATH("ENEMY", "images/enemy.png")
    PATH("DEFAULT", "fonts/default.ttf")
    PATH("CODE", "fonts/code.ttf")
    PATH("PENCIL", "fonts/pencil.ttf")
    PATH("SERIF", "fonts/serif.ttf")
    PATH("HANDWRITING", "fonts/handwriting.ttf")
    PATH("TYPEWRITER", "fonts/typewriter.ttf")
    PATH("JOINED", "fonts/joined.ttf")

    COLOR("WHITE", 1, 1, 1)
    COLOR("BLACK", 0, 0, 0)
    COLOR("GRAY", .5, .5, .5)
    COLOR("DARK_GRAY", .2, .2, .2)
    COLOR("LIGHT_GRAY", .8, .8, .8)
    COLOR("BROWN", .6, .2, .2)
    COLOR("TAN", .8, .7, .6)
    COLOR("RED", 1, 0, 0)
    COLOR("DARK_RED", .6, 0, 0)
    COLOR("SALMON", 1, .5, .5)
    COLOR("ORANGE", 1, .5, 0)
    COLOR("GOLD", 1, .8, 0)
    COLOR("YELLOW", 1, 1, 0)
    COLOR("OLIVE", .5, .5, 0)
    COLOR("LIME", 0, 1, 0)
    COLOR("DARK_GREEN", 0, .4, 0)
    COLOR("GREEN", 0, .5, 0)
    COLOR("AQUA", 0, 1, 1)
    COLOR("BLUE", 0, 0, 1)
    COLOR("LIGHT_BLUE", .5, .8, 1)
    COLOR("AZURE", .9, 1, 1)
    COLOR("NAVY", 0, 0, .5)
    COLOR("PURPLE", .5, 0, 1)
    COLOR("PINK", 1, .75, .8)
    COLOR("MAGENTA", 1, 0, 1)

    GLuint vertex = glCreateShader(GL_VERTEX_SHADER);
    GLuint fragment = glCreateShader(GL_FRAGMENT_SHADER);
    program = glCreateProgram();
    path[length] = 0;

    const char *vs =
        "#version 330 core\n"

        "in vec2 vert;"
        "in vec2 coord;"
        "out vec2 pos;"

        "uniform mat4 view;"
        "uniform mat4 obj;"

        "void main() {"
            "gl_Position = view * obj * vec4(vert, 0, 1);"
            "pos = coord;"
        "}";

    const char *fs =
        "#version 330 core\n"

        "in vec2 pos;"
        "out vec4 fragment;"

        "uniform vec4 color;"
        "uniform sampler2D sampler;"
        "uniform int img;"

        "void main() {"
            "if (img == " STR(TEXT) ") fragment = vec4(1, 1, 1, texture(sampler, pos).r) * color;"
            "else if (img == " STR(IMAGE) ") fragment = texture(sampler, pos) * color;"
            "else if (img == " STR(SHAPE) ") fragment = color;"
        "}";

    glShaderSource(vertex, 1, &vs, NULL);
    glShaderSource(fragment, 1, &fs, NULL);
    glCompileShader(vertex);
    glCompileShader(fragment);

    glAttachShader(program, vertex);
    glAttachShader(program, fragment);
    glDeleteShader(vertex);
    glDeleteShader(fragment);
    glLinkProgram(program);
    glUseProgram(program);

    uniform[vert] = glGetAttribLocation(program, "vert");
    uniform[coord] = glGetAttribLocation(program, "coord");
    uniform[view] = glGetUniformLocation(program, "view");
    uniform[obj] = glGetUniformLocation(program, "obj");
    uniform[color] = glGetUniformLocation(program, "color");
    uniform[img] = glGetUniformLocation(program, "img");

    GLuint buffer;
    GLfloat data[] = {-.5, .5, 0, 0, .5, .5, 1, 0, -.5, -.5, 0, 1, .5, -.5, 1, 1};

    glGenVertexArrays(1, &mesh);
    glBindVertexArray(mesh);
    glGenBuffers(1, &buffer);
    glBindBuffer(GL_ARRAY_BUFFER, buffer);
    glBufferData(GL_ARRAY_BUFFER, sizeof data, data, GL_STATIC_DRAW);

    glVertexAttribPointer(uniform[vert], 2, GL_FLOAT, GL_FALSE, sizeof(GLfloat) * 4, 0);
    glVertexAttribPointer(uniform[coord], 2, GL_FLOAT, GL_FALSE, sizeof(GLfloat) * 4, (void *) (sizeof(GLfloat) * 2));
    glEnableVertexAttribArray(uniform[vert]);
    glEnableVertexAttribArray(uniform[coord]);

    glBindVertexArray(0);
    glDeleteBuffers(1, &buffer);

    glEnable(GL_MULTISAMPLE);
    glEnable(GL_BLEND);

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1);
    glUniform1i(glGetUniformLocation(program, "sampler"), 0);

    return 0;
}

static void Module_free() {
    while (textures) {
        Texture *this = textures;
        glDeleteTextures(1, &this -> src);
        free(this -> name);

        textures = this -> next;
        free(this);
    }

    while (fonts) {
        Font *this = fonts;
        FT_Done_Face(this -> face);
        free(this -> name);

        fonts = this -> next;
        free(this);
    }

    glDeleteProgram(program);
    glDeleteVertexArrays(1, &mesh);

    FT_Done_FreeType(library);
    glfwTerminate();

    Py_XDECREF(loop);
    Py_DECREF(window);
    Py_DECREF(cursor);
    Py_DECREF(key);
    Py_DECREF(camera);
}

static PyMethodDef ModuleMethods[] = {
    {"random", Module_random, METH_VARARGS, "find a random number between two numbers"},
    {"randint", Module_randint, METH_VARARGS, "find a random integer between two integers"},
    {"sin", Module_sin, METH_O, "sine function of an angle"},
    {"cos", Module_cos, METH_O, "cosine function of an angle"},
    {"tan", Module_tan, METH_O, "tangent function of an angle"},
    {"sqrt", Module_sqrt, METH_O, "find the square root"},
    {"run", Module_run, METH_NOARGS, "activate the main game loop"},
    {NULL}
};

static PyModuleDef_Slot ModuleSlots[] = {
    {Py_mod_exec, Module_exec},
    {0, NULL}
};

static struct PyModuleDef Module = {
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = "JoBase",
    .m_size = 0,
    .m_free = Module_free,
    .m_methods = ModuleMethods,
    .m_slots = ModuleSlots
};

PyMODINIT_FUNC PyInit_JoBase() {
    printf("Welcome to JoBase\n");
    srand(time(NULL));

    READY(VectorType)
    READY(ButtonType)
    READY(CursorType)
    READY(KeyType)
    READY(CameraType)
    READY(WindowType)
    READY(BaseType)
    READY(RectangleType)
    READY(ImageType)
    READY(TextType)
    READY(CircleType)
    READY(LineType)
    READY(ShapeType)
    READY(PhysicsType)
    READY(JointType)
    READY(PinType)
    READY(PivotType)
    READY(MotorType)
    READY(SpringType)
    READY(GrooveType)

    return PyModuleDef_Init(&Module);
}