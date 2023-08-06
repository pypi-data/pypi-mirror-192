import setuptools, sys, os

extra_compile_args = []
extra_link_args = []
library_dirs = []
libraries = []

if sys.platform == "win32":
    libraries = [
        "glfw3", "opengl32", "kernel32", "user32", "gdi32", "winspool", "shell32",
        "ole32", "oleaut32", "uuid", "comdlg32", "advapi32", "freetype", "chipmunk"
    ]

    library_dirs = [
        "glfw/build/src/Release", "freetype/build/Release",
        "Chipmunk2D/build/src/Release"
    ]

elif sys.platform == "linux":
    libraries = [
        "glfw3", "GL", "m", "X11", "pthread", "Xi", "Xrandr", "dl", "rt", "png",
        "freetype", "z", "chipmunk"
    ]

    library_dirs = ["glfw/build/src", "freetype/build", "Chipmunk2D/build/src"]
    extra_compile_args = ["-Wextra", "-Wfloat-conversion"]

elif sys.platform == "darwin":
    extra_link_args = ["-framework", "OpenGL", "-framework", "IOKit", "-framework", "Cocoa"]
    library_dirs = ["glfw/build/src", "freetype/build", "Chipmunk2D/build/src"]
    libraries = ["glfw3", "freetype", "chipmunk", "bz2", "z"]

setuptools.setup(
    name = "JoBase",
    version = "2.6",
    author = "Reuben Ford",
    author_email = "hello@jobase.org",
    description = "Fast Python Game Library",
    long_description = open("README.md", "r").read(),
    long_description_content_type = "text/markdown",
    url = "https://jobase.org",
    python_requires = ">=3.6",
    license = "GPL-3.0-or-later",
    packages = ["JoBase"],
    package_data = {"JoBase": ["images/*.png", "fonts/*.ttf", "examples/**/*.py", "examples/*/README.md"]},
    include_package_data = True,

    keywords = [
        "fast", "beginner", "extension",
        "library", "opengl", "glfw",
        "games", "c", "children", "freetype"
    ],

    project_urls = {
        "Source": "https://github.com/JoBase/JoBase",
        "Documentation": "https://jobase.org/reference"
    },

    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    
    ext_modules = [
        setuptools.Extension(
            "JoBase.__init__",
            [os.path.join("src", e) for e in os.listdir("src")],

            extra_compile_args = extra_compile_args,
            extra_link_args = extra_link_args,
            library_dirs = library_dirs,
            libraries = libraries,

            include_dirs = [
                "include", "glfw/include", "freetype/include",
                "Chipmunk2D/include"
            ])
    ])
