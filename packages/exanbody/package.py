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
    version("v2.1.0",  tag='v2.1.0')
    version("v2.0.9",  tag='v2.0.9')
    version("v2.0.8",  tag='v2.0.8')
    version("v2.0.7",  tag='v2.0.7', preferred=True)
    version("v2.0.6",  tag='v2.0.6')
    version("v2.0.5",  tag='v2.0.5')
    version("v2.0.4",  tag='v2.0.4')
    version("v2.0.2",  tag='v2.0.2')
    version("v2.0.0",  tag='v2.0.0')

    # Variants
    variant("cuda"       , default=False, description="Support for GPU")
    variant("contrib_md" , default=False, description="Support for MD miniapp")
    variant("snap_fp32"  , default=False, description="Use FP32 math in the SNAP potential (contrib_md)")
    variant("contrib_pi" , default=False, description="Support for PI miniapp")        
    variant("contrib_egl", default=False, description="Support for EGL Rendering")        

    # Dependencies
    depends_on("cmake@3.31.0:")
    depends_on("yaml-cpp@0.6.3")
    depends_on("openmpi")
    depends_on("cuda", when="+cuda")
    depends_on("eglrenderer", when="+contrib_egl")
    
    # Main
    depends_on("onika@main", when="@main")
    
    # Versioning
    depends_on("onika@v1.1.0", when="@v2.1.0")
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
        "particle_int_type", 
        default="uint8_t", 
        values=("uint8_t", "uint16_t", "uint32_t"), 
        description='Integer type used for field::type')

    def cmake_args(self):
        args = [
            self.define_from_variant("EXANB_BUILD_CONTRIB_MD" , "contrib_md" ),
            self.define_from_variant("EXANB_BUILD_MICROSTAMP" , "contrib_md" ),
            self.define_from_variant("SNAP_FP32_MATH"         , "snap_fp32"  ),
            self.define_from_variant("EXANB_BUILD_CONTRIB_PI" , "contrib_pi" ),
            self.define_from_variant("EXANB_BUILD_MICROCOSMOS", "contrib_pi" ),
            self.define_from_variant("EXANB_BUILD_CONTRIB_EGL", "contrib_egl"),
            "-DXNB_PARTICLE_TYPE_INT={0}".format(self.spec.variants['particle_int_type'].value),
              ]
        return args
