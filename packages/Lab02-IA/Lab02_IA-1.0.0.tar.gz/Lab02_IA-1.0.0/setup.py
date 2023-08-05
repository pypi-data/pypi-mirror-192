from setuptools import find_packages, setup

setup(
    name="Lab02_IA",
    author ="Gabriela Contreras",
    python_requires=">=3.6",
    long_description = open("README.md").read(),
    long_description_content_type ="text/markdown",
    requires=["pgmpy"],
    entry_points={"console_scripts":["Lab02_IA=Lab02_IA.cli:main"]},
    packages= find_packages(where="src"),
    package_dir={"":"src","Lab02_IA":"src/Lab02_IA"},
    url="https://github.com/dele20361/Lab02-IA",
    version="1.0.0",
    
)


