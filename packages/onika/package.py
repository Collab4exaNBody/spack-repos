from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *

import os
import shutil

class Onika(CMakePackage):
    """Onika is runtime library.
    """

    homepage = "https://github.com/Collab4exaNBody/onika"
    git = "https://github.com/Collab4exaNBody/onika.git"

    # Versions
    version("main", branch='main')
    version("v1.1.0",  tag='v1.1.0')
    version("v1.0.6",  tag='v1.0.6')
    version("v1.0.5",  tag='v1.0.5')
    version("v1.0.4",  tag='v1.0.4', preferred=True)
    version("v1.0.2",  tag='v1.0.2')
    version("v1.0.0",  tag='v1.0.0')

    # Variants
    variant("cuda"    , default=False, description="Support for GPU")
    variant("contribs", default=False, description="Support for EGL Rendering")

    # Dependencies
    depends_on("cmake")
    depends_on("yaml-cpp@0.6.3")
    depends_on("openmpi")
    depends_on("cuda"       , when="+cuda")
    depends_on("eglrenderer", when="+contribs")
    
    default_build_system = "cmake"
    build_system("cmake", default="cmake")

    variant(
        "build_type",
        default="Release", 
        values=("Release", "Debug", "RelWithDebInfo"),
        description="CMake build type",
        )

    def cmake_args(self):
      args = [ self.define_from_variant("ONIKA_BUILD_CUDA", "cuda"), self.define_from_variant("ONIKA_BUILD_CONTRIBS", "contribs"), ]
      return args
