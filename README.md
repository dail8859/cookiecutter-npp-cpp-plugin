# cookiecutter-npp-cpp-plugin

[![Build status](https://ci.appveyor.com/api/projects/status/rgv7n4sjfld3pysl?svg=true)](https://ci.appveyor.com/project/dail8859/cookiecutter-npp-cpp-plugin)

A [cookiecutter](https://github.com/audreyr/cookiecutter) C++ Notepad++ plugin template.

## Usage

1. Install [Notepad++ v7.7](https://notepad-plus-plus.org/) (or later)
1. Install [Python](https://www.python.org/) (if not installed already)
1. From a command prompt, run:
```
pip install cookiecutter
cookiecutter https://github.com/dail8859/cookiecutter-npp-cpp-plugin.git
```
4. You will be asked some basic info (project name, description, etc.) for the new plugin.
5. Open the newly created `.sln` file with Visual Studio.
6. Press `F5` and enjoy.

Visual Studio will build and copy the newly created DLL file into plugin directory of Notepad++. It will also start the Notepad++ application for debugging, meaning you can set breakpoints and step through your plugin source code.
