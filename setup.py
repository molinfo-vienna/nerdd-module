from setuptools import find_packages, setup

# some RDKit versions are not recognized by setuptools
# -> check if RDKit is installed by attempting to import it
# -> if RDKit can be imported, do not add it to install_requires
rdkit_installed = False
try:
    import rdkit

    rdkit_installed = True
except ModuleNotFoundError:
    pass

# rdkit 2022.3.3 is the oldest (reasonable) version
rdkit_requirement = ["rdkit>=2022.3.3"] if not rdkit_installed else []

setup(
    name="nerdd-module",
    version="0.2.5",
    maintainer="Steffen Hirte",
    maintainer_email="steffen.hirte@univie.ac.at",
    packages=find_packages(),
    url="https://github.com/molinfo-vienna/nerdd-module.git",
    description="Base package to create NERDD modules",
    license="BSD 3-Clause License",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=rdkit_requirement
    + [
        "pandas>=1.2.1",
        "pyyaml>=6.0",
        "filetype~=1.2.0",
        "rich-click>=1.7.1",
        "stringcase>=1.2.0",
        "decorator>=5.1.1",
        # install importlib-resources and importlib-metadata for old Python versions
        "importlib-resources>=5; python_version<'3.10'",
        "importlib-metadata>=4.6; python_version<'3.10'",
        # note: version 1.0.0 of chembl_structure_pipeline is not available on pypi,
        # but it could potentially be installed from github
        "chembl_structure_pipeline>=1.0.0",
    ],
    extras_require={
        "dev": [],
        "test": [
            "pytest",
            "pytest-sugar",
            "pytest-cov",
            "pytest-asyncio",
            "pytest-bdd",
            "pytest-mock",
            "pytest-watch",
            "hypothesis",
            "hypothesis-rdkit",
        ],
        "docs": [
            "mkdocs",
            "mkdocs-material",
            "mkdocstrings",
        ],
    },
    classifiers=[
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: C",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Scientific/Engineering",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
