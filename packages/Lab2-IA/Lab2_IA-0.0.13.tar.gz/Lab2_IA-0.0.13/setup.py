from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "0.0.13"
DESCRIPTION = "R bayesianas"
LONG_DESCRIPTION = "Este packete permite escribir uyna red bayesiana en un archivo txt y hacer inferencia probabilista con la misma"

# Setting up
setup(
    name="Lab2_IA",
    version=VERSION,
    author="Maria Isabel Solano,Roberto Vallecillos, Diego Cordova, Alejandro Gomez",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["opencv-python", "pyautogui", "pyaudio"],
    keywords=["python", "bayesian", "statistics"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
