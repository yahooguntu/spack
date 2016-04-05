from spack import *
import os

class Pgi(Package):
    """PGI optimizing multi-core x64 compilers for Linux, MacOS & Windows
    with support for debugging and profiling of local MPI processes.

    Note: The PGI compilers are licensed software. You will need to create
    an account on the PGI homepage and download PGI yourself. Once the download
    finishes, rename the file (which may contain information such as the
    architecture) to the format: pgi-<version>.tar.gz. Spack will search your
    current directory for a file of this format. Alternatively, add this
    file to a mirror so that Spack can find it. For instructions on how to
    set up a mirror, see http://software.llnl.gov/spack/mirrors.html"""

    homepage = "http://www.pgroup.com/"
    url      = "file://%s/pgi-16.3.tar.gz" % os.getcwd()

    version('16.3', '618cb7ddbc57d4e4ed1f21a0ab25f427')

    variant('network', default=True,  description="Perform a network install")
    variant('single',  default=False, description="Perform a single system install")
    variant('nvidia',  default=False, description="Enable installation of optional NVIDIA components, such as CUDA")
    variant('amd',     default=False, description="Enable installation of optional AMD components")
    variant('java',    default=False, description="Enable installation of Java Runtime Environment")
    variant('mpi',     default=False, description="Enable installation of Open MPI")

    # Licensing
    license_required = True
    license_comment  = '#'
    license_files    = ['license.dat']
    license_vars     = ['PGROUPD_LICENSE_FILE', 'LM_LICENSE_FILE']
    license_url      = 'http://www.pgroup.com/doc/pgiinstall.pdf'


    def install(self, spec, prefix):
        # Enable the silent installation feature
        os.environ['PGI_SILENT'] = "true"
        os.environ['PGI_ACCEPT_EULA'] = "accept"
        os.environ['PGI_INSTALL_DIR'] = prefix

        if '+network' in spec and '~single' in spec:
            os.environ['PGI_INSTALL_TYPE'] = "network"
            os.environ['PGI_INSTALL_LOCAL_DIR'] = "%s/%s/share_objects" % (prefix, self.version)
        elif '+single' in spec and '~network' in spec:
            os.environ['PGI_INSTALL_TYPE'] = "single"
        else:
            msg  = 'You must choose either a network install or a single system install.\n'
            msg += 'You cannot choose both.'
            raise RuntimeError(msg)

        if '+nvidia' in spec:
            os.environ['PGI_INSTALL_NVIDIA'] = "true"

        if '+amd' in spec:
            os.environ['PGI_INSTALL_AMD'] = "true"

        if '+java' in spec:
            os.environ['PGI_INSTALL_JAVA'] = "true"

        if '+mpi' in spec:
            os.environ['PGI_INSTALL_MPI'] = "true"

        # Run install script
        os.system("./install")
