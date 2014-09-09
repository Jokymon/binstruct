REM Run this script from the base directory of the binstruct project

REM Make sure you set the following variable to match with the corresponding
REM entry in your .pypirc
set TARGET_REPO=pypi

py -3 setup.py build --plat-name=win32 bdist_wininst --target-version 3.4 upload -r %TARGET_REPO%
py -3 setup.py build --plat-name=win-amd64 bdist_wininst --target-version 3.4 upload -r %TARGET_REPO%
py -3 setup.py build --plat-name=win-ia64 bdist_wininst --target-version 3.4 upload -r %TARGET_REPO%
py -3 setup.py sdist bdist_egg upload -r %TARGET_REPO%

py -2 setup.py build --plat-name=win32 bdist_wininst --target-version 2.7 upload -r %TARGET_REPO%
py -2 setup.py build --plat-name=win-amd64 bdist_wininst --target-version 2.7 upload -r %TARGET_REPO%
py -2 setup.py build --plat-name=win-ia64 bdist_wininst --target-version 2.7 upload -r %TARGET_REPO%
py -2 setup.py bdist_egg upload -r %TARGET_REPO%

