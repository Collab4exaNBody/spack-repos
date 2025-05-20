from spack import *

class Exasph(CMakePackage):
    """ExaSPH is a SPH Simulation Code using the ExaNBody framework.
    """

    homepage = "https://github.com/Collab4exaNBody/exaSPH"
    git = "https://github.com/Collab4exaNBody/exaSPH.git"

    version("1.0.0", git='git@github.com:Collab4exaNBody/exaSPH.git', branch='v1.0.0-rdev', preferred=True )
    variant("cuda", default=False, description="Support for GPU")

    depends_on("cmake@3.27.9")
    depends_on("yaml-cpp@0.6.3")
    depends_on("openmpi")
    depends_on("exanbody@v2.0.2", when="@1.0.0")
    depends_on("exanbody+cuda", when="+cuda")
    build_system("cmake", default="cmake")

    def cmake_args(self):
        args = [ ]
        return args
