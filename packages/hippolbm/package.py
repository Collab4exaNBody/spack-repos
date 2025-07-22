from spack import *

class Hippolbm(CMakePackage):
    """HippoLNM is a LBM Simulation Code.
		"""

    homepage = "https://github.com/Collab4exaNBody/hippoLBM"
    git = "https://github.com/Collab4exaNBody/hippoLBM.git"

    version("main", git='https://github.com/Collab4exaNBody/hippoLBM.git',  branch='main') 
    version("0.1.0", git='https://github.com/Collab4exaNBody/hippoLBM.git',  tag='v0.1.0', preferred=True ) 

    variant("cuda", default=False, description="Support for GPU")

    depends_on("cmake@3.27.9")
    depends_on("yaml-cpp@0.6.3")
    depends_on("openmpi")
    depends_on("onika+cuda", when="+cuda")	
	
# main
    depends_on("onika@v1.0.4", when="@main")
    depends_on("onika@v1.0.4", when="@0.1.0")
    build_system("cmake", default="cmake")

    def setup_run_environment(self, env):
        env.set('hippoLBM_DIR', self.prefix)


    def cmake_args(self):
        args = []
        return args
