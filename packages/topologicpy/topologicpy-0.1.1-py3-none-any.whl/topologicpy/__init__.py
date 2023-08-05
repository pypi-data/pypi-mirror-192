import sys
import os, re
from sys import platform

__version__ = '0.1.1'
__version_info__ = tuple([ int(num) for num in __version__.split('.')])

if platform == 'win32':
    os_name = 'windows'
else:
    os_name = 'linux'

sitePackagesFolderName = os.path.join(os.path.dirname(os.path.realpath(__file__)), "bin", os_name)
topologicFolderName = "topologic"
topologicPath = os.path.join(sitePackagesFolderName, topologicFolderName)
sys.path.append(topologicPath)

import topologic

