from os import makedirs, system
import sys
import shutil

# Numerous portability in this file are now being handled with this standard library
# Python 3.x compatibility only
# https://docs.python.org/3/library/pathlib.html
from pathlib import Path

# get local environment using sys.prefix
libPath = Path(sys.prefix) / "lib" / "site-packages"

# Hack to get around problematic updating of distutils installed PyYAML and a slightly older pandas requiring a compatible numpy
pyYamlPath = libPath / "PyYaml"
numpyPath = libPath / "numpy"

# rmtree implements using 'os' abstractions, which take "path-like" objects incl. Path
shutil.rmtree(pyYamlPath, ignore_errors=True)
shutil.rmtree(numpyPath, ignore_errors=True)

# We can't use the `..` selector in `pathlib`.
# So here, convert the script directory into an absolute path and get its parent.
# TODO: Although generally speaking we shouldn't need to reference other parts of the project in this way.
mvpModuleLibPath = Path(".").resolve().parent / "mvp-module-library"
if mvpModuleLibPath.exists():
    sys.path.append(str(mvpModuleLibPath))
    # Install pip requirements
    system("{0} -m pip install -r requirements.txt".format(sys.executable))