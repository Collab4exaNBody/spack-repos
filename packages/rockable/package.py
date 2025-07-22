from spack import *

class Rockable(CMakePackage):
    """Rockable is a DEM Simulation Code.
		"""

    homepage = "https://github.com/richefeu/rockable"
    git = "https://github.com/richefeu/rockable.git"

    version("main", git='https://github.com/richefeu/rockable.git',  branch='main') 
 
    variant("see", default=True, description="Compile the glut application to visualize the conf-files")
    variant("see2", default=False, description="Compile the glfw application to visualize the conf-files")
    variant("see3", default=False, description="Compile the application to edit graphically the input files")
    variant("postpro", default=False, description="Compile the application to run post-processing commands")
    variant("prepro", default=True, description="Compile the preprocessing tools")
    variant("conftovtk", default=True, description="Convert conf files to VTK")

    depends_on("cmake@3.27.9")
    depends_on("opengl" , when="+see")
#    depends_on("mesa-glu", when="+see")
    depends_on("libpng", when="+see")
#    depends_on("openglu@1.3", when="+see")
#    depends_on("freeglut", when="+see")
    depends_on("glfw" , when="+see3")
    depends_on("glfw" , when="+see2")
    depends_on("pkg-config")

    def setup_run_environment(self, env):
        env.set('rockable_DIR', self.prefix)

    def cmake_args(self):
        args = [self.define_from_variant("ROCKABLE_COMPILE_SEE", "see"), self.define_from_variant("ROCKABLE_COMPILE_SEE2", "see2") , self.define_from_variant("ROCKABLE_COMPILE_SEE3", "see3") , self.define_from_variant("ROCKABLE_COMPILE_POSTPRO", "postpro") , self.define_from_variant("ROCKABLE_COMPILE_PREPRO", "prepro") , self.define_from_variant("ROCKABLE_COMPILE_CONF2VTK", "conftovtk") ]
        return args
