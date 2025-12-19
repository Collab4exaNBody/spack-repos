from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *

import os
import shutil

class Exanbody(CMakePackage):
    """ExaNBody is a N-Body framework.
    """

    homepage = "https://github.com/Collab4exaNBody/exaNBody"
    git = "https://github.com/Collab4exaNBody/exaNBody.git"

    version("main",  git='https://github.com/Collab4exaNBody/exaNBody.git', branch='main')
    version("v2.0.7",  tag='v2.0.7', preferred=True)
    version("v2.0.6",  tag='v2.0.6')
    version("v2.0.5",  tag='v2.0.5')
    version("v2.0.4",  tag='v2.0.4')
    version("v2.0.2",  tag='v2.0.2')
    version("v2.0.0",  tag='v2.0.0')

    depends_on("onika@main", when="@main")
    depends_on("onika@v1.0.4", when="@v2.0.6")
    depends_on("onika@v1.0.4", when="@v2.0.5")
    depends_on("onika@v1.0.4", when="@v2.0.4")
    depends_on("onika@v1.0.2", when="@v2.0.2")
    depends_on("onika@v1.0.0", when="@v2.0.0")
    depends_on("onika+cuda", when="+cuda")
    depends_on("cmake")
    variant("cuda", default=False, description="Support for GPU")
    variant("contribs", default=False, description="Support for MD miniapp")
    depends_on("yaml-cpp")
    depends_on("cuda", when="+cuda")
#    build_system("cmake", "autotools", default="cmake")
    
    default_build_system = "cmake"
    build_system("cmake", default="cmake")

    def setup_run_environment(self, env):
        env.set('exaNBody_DIR', self.prefix)

    variant(
        "build_type",
        default="Release", 
        values=("Release", "Debug", "RelWithDebInfo"),
        description="CMake build type",
        )

    def cmake_args(self):
      args = [self.define_from_variant("EXANB_BUILD_CONTRIB_MD=ON", "contribs"),
              self.define_from_variant("EXANB_BUILD_MICROSTAMP=ON", "contribs"),
              self.define_from_variant("EXANB_BUILD_CONTRIB_PI=ON", "contribs"),
              self.define_from_variant("EXANB_BUILD_MICROCOSMOS=ON", "contribs"),
              ]
      return args
