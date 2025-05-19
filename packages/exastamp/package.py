from spack import *

class Exastamp(CMakePackage):
    """ExaSTAMP is a MD Simulation Code using the ExaNBody framework.
    """

    homepage = "https://github.com/Collab4exaNBody/exaStamp"
    git = "https://github.com/Collab4exaNBody/exaStamp.git"

    version("3.7.0-rdev", git='git@github.com:Collab4exaNBody/exaStamp.git', branch='v3.7.0-rdev', preferred=True )
    variant("cuda", default=False, description="Support for GPU")

    depends_on("cmake@3.27.9")
    depends_on("yaml-cpp@0.6.3")
    depends_on("openmpi")
    depends_on("exanbody@v2.0.2", when="@3.7.0-rdev")
    depends_on("exanbody+contribs")
    depends_on("exanbody+cuda", when="+cuda")
#    depends_on("onika+cuda", when="+cuda")
    build_system("cmake", default="cmake")

    # @run_before("install")
    # def pre_install(self):
    #     with working_dir(self.build_directory):
    #         # When building shared libraries these need to be installed first
    #         if self.spec.version <= Version("1.0.2"):
    #           make("UpdatePluginDataBase")

    def cmake_args(self):
        args = [ "-DONIKA_BUILD_exaStampLCHBOP=OFF",
                 "-DONIKA_BUILD_exaStampMolecule=OFF",
                 "-DONIKA_BUILD_exaStampMolecule=OFF",
                 "-DONIKA_BUILD_exaStampRigidMolecule=OFF",
                 "-DONIKA_BUILD_exaStampSnap=OFF",
                 "-DONIKA_BUILD_exaStampSnapLegacy=OFF",
                 "-DONIKA_BUILD_exaStampMechanical=OFF"
                ]
        return args
