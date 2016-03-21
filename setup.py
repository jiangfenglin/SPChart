# A setup script showing how to extend py2exe.
#
# In this case, the py2exe command is subclassed to create an installation
# script for InnoSetup, which can be compiled with the InnoSetup compiler
# to a single file windows installer.
#
# By default, the installer will be created as dist\Output\setup.exe.

from distutils.core import setup
import py2exe
import sys
import os
import time
import shutil
import matplotlib
from distutils.filelist import findall



################################################################
# A program using wxPython

# The manifest will be inserted as resource into test_wx.exe.  This
# gives the controls the Windows XP appearance (if run on XP ;-)
#
# Another option would be to store if in a file named
# test_wx.exe.manifest, and probably copy it with the data_files
# option.
#

# Remove the build folder
shutil.rmtree("build", ignore_errors=True)

# do the same for dist folder
shutil.rmtree("dist", ignore_errors=True)


manifest_template = '''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity
    version="5.0.0.0"
    processorArchitecture="x86"
    name="%(prog)s"
    type="win32"
  />
  <description>%(prog)s</description>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel
            level="asInvoker"
            uiAccess="false">
        </requestedExecutionLevel>
      </requestedPrivileges>
    </security>
  </trustInfo>
  <dependency>
    <dependentAssembly>
      <assemblyIdentity
            type="win32"
            name="Microsoft.VC90.CRT"
            version="9.0.21022.8"
            processorArchitecture="x86"
            publicKeyToken="1fc8b3b9a1e18e3b">
      </assemblyIdentity>
    </dependentAssembly>
  </dependency>
  <dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
  </dependency>
</assembly>
'''

RT_MANIFEST = 24

################################################################
# arguments for the setup() call

Myprog_wx = dict(
    script = "SPchart.pyw",
    other_resources = [(RT_MANIFEST, 1, manifest_template % dict(prog="SPchart"))],
    #dest_base = r"prog\Myprog_wx",
    icon_resources= [(1, "icons/icon.ico")]
    )


zipfile = r"lib\shardlib"


#includes = ['sip','matplotlib.backends','matplotlib.backends.backend_wxagg','matplotlib.backends.backend_wx',
#            'matplotlib.numerix.ma','matplotlib.numerix.fft','matplotlib.numerix.linear_algebra','matplotlib.numerix.mlab','matplotlib.numerix.random_array'
#           ]
includes = []#['matplotlib.backends','matplotlib.backends.backend_wxagg','matplotlib.backends.backend_wx',
           # 'matplotlib.numerix.ma','matplotlib.numerix.fft','matplotlib.numerix.linear_algebra','matplotlib.numerix.mlab','matplotlib.numerix.random_array'
           #]

excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'pywin.debugger',
            'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
            'Tkconstants', 'Tkinter', 'pydoc', 'doctest', 'test', 'sqlite3',
            'PyQt4','_ssl'
            ]
dll_excludes = ['libgdk-win32-2.0-0.dll','libgobject-2.0-0.dll',
                'tcl84.dll','tk84.dll','libglib-2.0-0.dll','libgdk_pixbuf-2.0-0.dll',
                'tcl85.dll','tk85.dll','intl.dll','jpeg62.dll','pywintypes26.dll','MSVCP90.dll']
options = {"py2exe": 
            {   
                "includes" : includes,
                'excludes': excludes,
                "dll_excludes": dll_excludes,
                'packages' : ['matplotlib', 'pytz'],
                "compressed": 1,                
                #"optimize": 2,
                "bundle_files": 2
            }
          }

################################################################
import os

class InnoScript:
    def __init__(self,
                 name,
                 lib_dir,
                 dist_dir,
                 windows_exe_files = [],
                 lib_files = [],
                 version = "0.0"):
        self.lib_dir = lib_dir
        self.dist_dir = dist_dir
        if not self.dist_dir[-1] in "\\/":
            self.dist_dir += "\\"
        self.name = name
        self.version = version
        self.windows_exe_files = [self.chop(p) for p in windows_exe_files]
        self.lib_files = [self.chop(p) for p in lib_files]

    def chop(self, pathname):
        assert pathname.startswith(self.dist_dir)
        return pathname[len(self.dist_dir):]
    
    def create(self, pathname="dist\\SPchart.iss"):
        self.pathname = pathname
        ofi = self.file = open(pathname, "w")
        print >> ofi, "; WARNING: This script has been created by py2exe. Changes to this script"
        print >> ofi, "; will be overwritten the next time py2exe is run!"
        print >> ofi, r"[Setup]"
        print >> ofi, r"AppName=%s" % self.name
        print >> ofi, r"AppVerName=%s %s" % (self.name, self.version)
        print >> ofi, r"AppPublisher=Aaron Lee"
        print >> ofi, r"DefaultDirName={pf}\SPchart\%s" % self.name
        print >> ofi, r"DefaultGroupName=SPchart" #% self.name
        print >> ofi, r"AppPublisherURL=http://www.signal-integrity.org"
        print >> ofi, r"AppVersion=0.0"
        print >> ofi, r"OutputBaseFilename=%s_setup_%s" % (self.name,time.strftime("%Y%m%d"))
        print >> ofi

        print >> ofi, r"[Tasks]"
        print >> ofi, r'Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked'
        print >> ofi, r'Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked'
        

        print >> ofi, r"[Files]"
        for path in self.windows_exe_files + self.lib_files:
            print >> ofi, r'Source: "%s"; DestDir: "{app}\%s"; Flags: ignoreversion' % (path, os.path.dirname(path))

        # add files in data dirs
        for d in dirs:
            print >> ofi, r'Source: "%s\%s\*"; DestDir: "{app}\%s"; Flags: ignoreversion' % (os.getcwd(),d, d)

        print >> ofi

        print >> ofi, r"[Icons]"
        for path in self.windows_exe_files:
            print >> ofi, r'Name: "{group}\%s"; Filename: "{app}\%s"; WorkingDir: {app}' % \
                  (self.name, path)
        print >> ofi, r'Name: "{group}\Uninstall %s"; Filename: "{uninstallexe}"; WorkingDir: {app}' % self.name

        print >> ofi, r'Name: "{commondesktop}\%s"; Filename: "{app}\%s"; Tasks: desktopicon; WorkingDir: {app}' % \
                  (self.name, path)

        print >> ofi, r'Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\%s"; Filename: "{app}\%s"; Tasks: quicklaunchicon; WorkingDir: {app}'% \
                  (self.name, path)


        #print >> ofi, "WorkingDir: {app}"

    def compile(self):
        try:
            import ctypes
        except ImportError:
            try:
                import win32api
            except ImportError:
                import os
                os.startfile(self.pathname)
            else:
                print "Ok, using win32api."
                win32api.ShellExecute(0, "compile",
                                                self.pathname,
                                                None,
                                                None,
                                                0)
        else:
            print "Cool, you have ctypes installed."
            res = ctypes.windll.shell32.ShellExecuteA(0, "compile",
                                                      self.pathname,
                                                      None,
                                                      None,
                                                      0)
            if res < 32:
                raise RuntimeError, "ShellExecute failed, error %d" % res


################################################################

from py2exe.build_exe import py2exe

class build_installer(py2exe):
    # This class first builds theo exe file(s), then creates a Windows installer.
    # You need InnoSetup for it.
    def run(self):
        # First, let py2exe do it's work.
        py2exe.run(self)

        lib_dir = self.lib_dir
        dist_dir = self.dist_dir
        
        # create the Installer, using the files py2exe has created.
        script = InnoScript("SPchart",
                            lib_dir,
                            dist_dir,
                            self.windows_exe_files,
                            self.lib_files)
        print "*** creating the inno setup script***"
        script.create()
        print "*** compiling the inno setup script***"
        script.compile()
        # Note: By default the final setup.exe will be in an Output subdirectory.

################################################################
import shutil
def my_copytree(src, dst):
    """Recursively copy a directory tree using copy2().

    Modified from shutil.copytree

    """
    base = os.path.basename(src)
    dst = os.path.join(dst, base)
    names = os.listdir(src)
    if not os.path.exists(dst):
        os.makedirs(dst)
    for name in names:
        srcname = os.path.join(src, name)
        try:
            if os.path.isdir(srcname):
                my_copytree(srcname, dst)
            else:
                shutil.copy2(srcname, dst)
        except:
#            error.traceback()
            raise
#copy other resource folders
dirs = ["icons","rc","Example"]
for d in dirs:
    my_copytree(d, 'dist')



matplotlibdatadir = matplotlib.get_data_path()
matplotlibdata = findall(matplotlibdatadir)
matplotlibdata_files = []
for f in matplotlibdata:
    dirname = os.path.join('mpl-data', f[len(matplotlibdatadir)+1:])
    matplotlibdata_files.append((os.path.split(dirname)[0], [f]))


setup(
    version = "0.0",
    description = "SPchart",
    name = "SPchart",
    author = "Aaron Lee",
    author_email = "leeooox@gmail.com",
    options = options,
    # The lib directory contains everything except the executables and the python dll.
    zipfile = zipfile,
    windows = [Myprog_wx],
    data_files = matplotlibdata_files,
    
    #data_files = [
    #            ('', []),],

    # use out build_installer class as extended py2exe build command
    cmdclass = {"py2exe": build_installer},
    )
