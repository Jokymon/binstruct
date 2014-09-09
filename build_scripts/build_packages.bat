REM Run this script from the base directory of the binstruct project

py -3 setup.py build --plat-name=win32 bdist_wininst --target-version 3.4
py -3 setup.py build --plat-name=win-amd64 bdist_wininst --target-version 3.4
py -3 setup.py build --plat-name=win-ia64 bdist_wininst --target-version 3.4
py -3 setup.py sdist bdist_egg

py -2 setup.py build --plat-name=win32 bdist_wininst --target-version 2.7
py -2 setup.py build --plat-name=win-amd64 bdist_wininst --target-version 2.7
py -2 setup.py build --plat-name=win-ia64 bdist_wininst --target-version 2.7
py -2 setup.py bdist_egg

