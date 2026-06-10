from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *

import os
import shutil

class Eglrenderer(CMakePackage):
    """EGLRender is a lightweight EGL interface for embedded GL rendering
       with no other dependencies than EGL/OpenGL Intended for on-screen
       and off-screen GPU rendering with no fancy dependencies.runtime library.
    """
    
    homepage = "https://github.com/carrardt/EGLRender"
    git = "https://github.com/carrardt/EGLRender.git"
    
    # Versions
    version("main", branch='main', preferred=True)
    
    # Variants
    variant("cuda",     default=False, description="Support for GPU")
    
    # Dependencies
    depends_on("cmake")
    depends_on("mesa")
    depends_on("cuda", when="+cuda")
    
    default_build_system = "cmake"
    build_system("cmake", default="cmake")
    
    variant(
        "build_type",
        default="Release", 
        values=("Release", "Debug", "RelWithDebInfo"),
        description="CMake build type",
    )
    
    def cmake_args(self):
        args = [ self.define_from_variant("EGLRENDER_GPU_COMPUTE_API=CUDA", "cuda"), ]
        return args
    
    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path(
            'CMAKE_PREFIX_PATH',
            os.path.join(self.prefix, 'lib', 'cmake')
        )  
