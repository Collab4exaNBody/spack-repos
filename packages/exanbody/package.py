from spack import *

class Exanbody(CMakePackage):
    """ExaNBody is a N-Body framework.
    """

    homepage = "https://github.com/Collab4exaNBody/exaNBody"
    git = "https://github.com/Collab4exaNBody/exaNBody.git"

    version("main",  git='https://github.com/Collab4exaNBody/exaNBody.git', branch='main')
    version("v2.0.4",  git='https://github.com/Collab4exaNBody/exaNBody.git', tag='v2.0.4', preferred=True)
    version("v2.0.2",  git='https://github.com/Collab4exaNBody/exaNBody.git', tag='v2.0.2')
    version("v2.0.0",  git='https://github.com/Collab4exaNBody/exaNBody.git', tag='v2.0.0')

    depends_on("onika@main", when="@main")
    depends_on("onika@v1.0.2", when="@v2.0.4")
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
      args = [self.define_from_variant("EXANB_BUILD_CONTRIB_MD=ON", "contribs"), self.define_from_variant("EXANB_BUILD_MICROSTAMP=ON", "contribs"), ]
      return args
