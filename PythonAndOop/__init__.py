import os
import re
files=os.listdir('.')

packages_needed=[package[:-3] for package in files[1:-5]]
__all__= packages_needed
print(__all__)

print(os.path.dirname(__file__))