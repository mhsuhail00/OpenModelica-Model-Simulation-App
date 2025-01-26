from cx_Freeze import setup, Executable
import sys
sys.setrecursionlimit(5000)

# Build options
build_options = {
    "packages": ["os", "sys", "pandas", "matplotlib", "PyQt6"],
    "includes": ["logic.plotting", "logic.execution", "logic.popups", "util.custom_widgets"],
    "excludes": [
        "tkinter",
    ],
    "include_files": [
        "resources/",
    ],
    "include_msvcr": True,
}

# Define the executable
executables = [
    Executable(
        "main.py",                 # Your main Python file
        base="Win32GUI",       # Use "Win32GUI" to suppress the console window
        target_name="SimulationApp.exe", # Name of the generated .exe file
        icon="resources/logo.ico",       # Icon for the .exe file
    )
]

# Setup function
setup(
    name="OpenModelica GUI",
    version="1.0",
    description="A GUI for simulation of OpenModelica Model Executable",
    options={"build_exe": build_options},
    executables=executables,
)
