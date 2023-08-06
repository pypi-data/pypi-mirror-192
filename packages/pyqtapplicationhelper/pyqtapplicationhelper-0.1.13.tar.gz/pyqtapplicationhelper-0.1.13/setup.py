from os import getcwd, walk
from os.path import join

from typing import List

from setuptools import setup
from pyqtapplicationhelper import __version__, __module_name__

def get_dependancies() -> List[str]:
    """Gets dependancies from requirements.txt"""
    dependancies = []

    requirements_file = join(getcwd(), "requirements.txt")

    with open(requirements_file,"r", encoding="UTF-8") as file:
        dependancies = file.read().split("\n")
        dependancies = filter(None, dependancies)
        dependancies = filter(bool, dependancies)
        dependancies = filter(len, dependancies)
        dependancies = list(filter(None, dependancies))

    return dependancies

def get_packages() -> List[str]:
    """Gets all subpackages"""
    directory = join(".","pyqtapplicationhelper")

    _packages = [x[0].replace("\\",".") for x in walk(directory) if "__pycache__" not in x[0]]

    return _packages

setup(
    name = __module_name__,
    version = __version__,
    author = "michaeldcanady",
    author_email = "",
    description = (""),
    license = "MIT",
    #keywords = "example documentation tutorial",
    url = "https://github.com/michaeldcanady/pyqtapplicationhelper",
    packages=get_packages(),
    install_requires=get_dependancies()
    #long_description=read('README'),
)