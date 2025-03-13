from spack import *

class Exanbody(CMakePackage):
    """ExaNBody is a N-Body framework.
    """

    homepage = "https://github.com/Collab4exaNBody/exaNBody"
    git = "https://github.com/Collab4exaNBody/exaNBody.git"


    version("main",  git='https://github.com/Collab4exaNBody/exaNBody.git', branch='main', preferred=True)
    version("exadem-exanbody-2.0",  git='https://github.com/Collab4exaNBody/exaNBody.git', tag='exadem-exanbody-2.0')
    version("release-2.0",  git='https://github.com/Collab4exaNBody/exaNBody.git', tag='release-2.0')

    depends_on("onika@main", when="@main")
    depends_on("onika@exadem-exanbody-2.0", when="@exadem-exanbody-2.0")
    depends_on("onika+cuda", when="+cuda")
    depends_on("cmake")
    variant("cuda", default=False, description="Support for GPU")
    depends_on("yaml-cpp")
    depends_on("cuda", when="+cuda")
#    build_system("cmake", "autotools", default="cmake")
    
    default_build_system = "cmake"
    build_system("cmake", default="cmake")

    variant(
        "build_type",
        default="Release", 
        values=("Release", "Debug", "RelWithDebInfo"),
        description="CMake build type",
        )

    def cmake_args(self):
      args = [ ]
      return args
