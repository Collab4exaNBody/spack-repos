from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *

import os
import shutil

class Exastamp(CMakePackage):
    """ExaSTAMP is a MD Simulation Code using the ExaNBody framework.
    """

    homepage = "https://github.com/Collab4exaNBody/exaStamp"
    git      = "https://github.com/Collab4exaNBody/exaStamp.git"

    version('main', branch='main')
    version('3.7.4', branch='v3.7.4', preferred=True)
    version('3.7.3', branch='v3.7.3')
    version('3.7.2', branch='v3.7.2')
    version('3.7.0', branch='v3.7.0-rdev')
    variant("cuda", default=False, description="Support for GPU")

    depends_on("cmake@3.27.9")
    depends_on("yaml-cpp@0.6.3")
    depends_on("openmpi")
    depends_on("exanbody+contribs")
    depends_on("exanbody+cuda", when="+cuda")
    build_system("cmake", default="cmake")

# main
    depends_on("exanbody@main", when="@main")

# versioning
    depends_on("exanbody@v2.0.7", when="@3.7.4")
    depends_on("exanbody@v2.0.6", when="@3.7.3")
    depends_on("exanbody@v2.0.5", when="@3.7.2")
    depends_on("exanbody@v2.0.2", when="@3.7.0")    

    def setup_run_environment(self, env):
        env.set('exaStamp_DIR', self.prefix)

    def cmake_args(self):
        args = [ ]
        return args
