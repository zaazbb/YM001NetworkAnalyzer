import sys
from cx_Freeze import setup, Executable

from main import version

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    #"build_exe"
    "optimize": 2,
    #"excludes":['asyncio', 'email', 'html', 'http', 'logging', 'unittest', 'xml'],
    #"includes": ["multiprocessing"],
##    "packages": ["os"],
    "packages": ["serial"],
    #"namespace_packages"
    #"replace_paths"
    #"path"
    #"init_script"
    #"base"
##    "compressed": True,
##    "copy_dependent_files": True,
##    "create_shared_zip": False,
##    "append_script_to_exe": True,
##    "include_in_shared_zip": False,
##    "icon":'card_back.ico',
    #"constants"
    "include_files":[('更新记录.txt'),
                     ('使用说明.txt'),
                     ('run.bat'),
                     ('config.ini')], 
    "include_msvcr": True,
    #"zip_includes"
    #"bin_includes"
    #"bin_excludes"
    #"bin_path_includes"
    #"bin_path_excludes": ['PyQt5/doc', 'PyQt5/examples'],
    #"silent"
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "NetworkAnalyzer",
        version = version,
        description = "NetworkAnalyzer!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py",
##                                  base=base,
##                                  copyDependentFiles=True,
##                                  appendScriptToExe=True
                                  )])
