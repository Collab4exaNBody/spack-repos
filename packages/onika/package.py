from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *

import os
import shutil

class Onika(CMakePackage):
    """Onika is runtime library.
    """

    homepage = "https://github.com/Collab4exaNBody/onika"
    git = "https://github.com/Collab4exaNBody/onika.git"


    version("main", branch='main')
    version("v1.0.4",  tag='v1.0.4', preferred=True)
    version("v1.0.2",  tag='v1.0.2')
    version("v1.0.0",  tag='v1.0.0')

    depends_on("cmake")
    variant("cuda", default=False, description="Support for GPU")
    depends_on("yaml-cpp@0.6.3")
    depends_on("openmpi")
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
      args = [ self.define_from_variant("ONIKA_BUILD_CUDA", "cuda"), ]
      return args
