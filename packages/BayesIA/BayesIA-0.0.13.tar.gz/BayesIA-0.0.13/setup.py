from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.13'
DESCRIPTION = 'redes bayesianas'
LONG_DESCRIPTION = 'Esta libreria nos permite crear y generar nuestras propias redes bayesianas con sus nodos, aristas, valores y probabilidades'

# Setting up
setup(
    name="BayesIA",
    version=VERSION,
    author="riv19062",
    author_email="<eleanjulian@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['networkx'],
    keywords=['python', 'IA', 'bayes'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
) 
