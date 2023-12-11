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
    version="0.1.10",
    maintainer="Steffen Hirte",
    maintainer_email="steffen.hirte@univie.ac.at",
    packages=find_packages(),
    url="https://github.com/molinfo-vienna/nerdd-module.git",
    description="Base package to create NERDD modules",
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
        # install importlib-resources for old Python versions
        "importlib-resources>=6.1.1; python_version<'3.10'",
        # note: version 1.0.0 of chembl_structure_pipeline is not available on pypi,
        # but it could potentially be installed from github
        "chembl_structure_pipeline>=1.0.0",
    ],
    extras_require={
        "dev": [],
        "test": [
            "pytest",
            "pytest-cov",
            "pytest-asyncio",
            "pytest-bdd",
            "pytest-mock",
            "pytest-watch",
            "hypothesis",
            "hypothesis-rdkit",
        ],
    },
)
