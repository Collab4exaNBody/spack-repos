from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *

import os
import shutil

class Exanbody(CMakePackage):
    """ExaNBody is a N-Body framework.
    """

    homepage = "https://github.com/Collab4exaNBody/exaNBody"
    git = "https://github.com/Collab4exaNBody/exaNBody.git"

    # Versions
    version("main", branch='main')
    version("v2.0.7",  tag='v2.0.7', preferred=True)
    version("v2.0.6",  tag='v2.0.6')
    version("v2.0.5",  tag='v2.0.5')
    version("v2.0.4",  tag='v2.0.4')
    version("v2.0.2",  tag='v2.0.2')
    version("v2.0.0",  tag='v2.0.0')

    # Variants
    variant("cuda", default=False, description="Support for GPU")
    variant("contribs", default=False, description="Support for MD miniapp")    

    # Dependencies
    depends_on("cmake@3.27.9")
    depends_on("yaml-cpp@0.6.3")
    depends_on("openmpi")
    depends_on("cuda", when="+cuda")
    
    # Main
    depends_on("onika@main", when="@main")
    
    # Versioning
    depends_on("onika@v1.0.5", when="@v2.0.7")
    depends_on("onika@v1.0.4", when="@v2.0.6")
    depends_on("onika@v1.0.4", when="@v2.0.5")
    depends_on("onika@v1.0.4", when="@v2.0.4")
    depends_on("onika@v1.0.2", when="@v2.0.2")
    depends_on("onika@v1.0.0", when="@v2.0.0")
    depends_on("onika+cuda", when="+cuda")
    
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
    variant(
        'particle_int_type', 
        default='uint8_t', 
        values=('uint8_t', 'uint16_t', 'uint32_t'), 
        description='Integer type used for field::type')
    def cmake_args(self):
      args = [self.define_from_variant("EXANB_BUILD_CONTRIB_MD=ON", "contribs"),
              self.define_from_variant("EXANB_BUILD_MICROSTAMP=ON", "contribs"),
              self.define_from_variant("EXANB_BUILD_CONTRIB_PI=ON", "contribs"),
              self.define_from_variant("EXANB_BUILD_MICROCOSMOS=ON", "contribs"),
              self.define_from_variant("SNAP_CPU_USE_LOCKS=ON", "contribs"),
              self.define_from_variant("SNAP_FP32_MATH=OFF", "contribs"),
              "-DXNB_PARTICLE_TYPE_INT={0}".format(spec.variants['particle_int_type'].value)
              ]
      return args
