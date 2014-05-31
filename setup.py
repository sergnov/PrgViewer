from cx_Freeze import setup, Executable as cxExecutable
import platform, sys 

base = None
if sys.platform == "win32":    
    base = "Win32GUI" 

includeFiles = ['PRGViewer-logo.ico','1.prg','Readme-Ru.pdf']

build_exe_options = {    
    "base": base,    
    "compressed" : True,    
    "create_shared_zip" : True,    
    "packages": ["os", "tkinter", "random", "prgLibrary"],
    "icon": "PRGViewer-logo.ico",
    'include_files': includeFiles,
    #'includeMSVCR' : True,
} 

WIN_Target = cxExecutable(script = "PRGViewer.py",    
    targetName = "PRGViewer.exe",    
    compress = True,    
    appendScriptToLibrary = False,    
    appendScriptToExe = True,
    icon = "PRGViewer-logo.ico")
    
setup(  name = "PRGViewer",        
    version = "2.2.2",
    description = "PRGViewer by Novicov 2.2.2",
    options = {"build_exe": build_exe_options},        
    executables = [WIN_Target])