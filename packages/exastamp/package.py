from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *

import os
import shutil

class Exastamp(CMakePackage):
    """ExaSTAMP is a MD Simulation Code using the ExaNBody framework.
    """

    homepage = "https://github.com/Collab4exaNBody/exaStamp"
    git      = "https://github.com/Collab4exaNBody/exaStamp.git"

    # Versions
    version('main', branch='main')
    version('v3.8.0', branch='v3.8.0', preferred=True)
    version('v3.7.5', branch='v3.7.5')
    version('v3.7.4', branch='v3.7.4')
    version('v3.7.3', branch='v3.7.3')
    version('v3.7.2', branch='v3.7.2')
    variant("cuda" , default=False, description="Support for GPU")
    variant("mlips", default=False, description="Support for MLIPS - POD PACE etc...-")
    
    # Variants
    depends_on("exanbody+contrib_md")
    depends_on("exanbody+cuda", when="+cuda")

    # Dependencies
    depends_on("cmake")
    depends_on("yaml-cpp@0.6.3")
    depends_on("openmpi")
    
    # Main
    depends_on("exanbody@main", when="@main")

    # Versioning
    depends_on("exanbody@v2.1.0", when="@3.8.0")
    depends_on("exanbody@v2.0.8", when="@3.7.5")    
    depends_on("exanbody@v2.0.7", when="@3.7.4")
    depends_on("exanbody@v2.0.6", when="@3.7.3")
    depends_on("exanbody@v2.0.5", when="@3.7.2")
    depends_on("exanbody@v2.0.2", when="@3.7.0")    

    build_system("cmake", default="cmake")
    
    def setup_run_environment(self, env):
        env.set('exaStamp_DIR', self.prefix)

    def cmake_args(self):
        args = [
            self.define_from_variant("EXASTAMP_BUILD_PACE", "mlips" ),
            self.define_from_variant("EXASTAMP_BUILD_POD" , "mlips" ),            
        ]
        return args
