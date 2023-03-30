# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="permedcoe",
    version="0.0.10",
    description="This package provides the common interface for the Building Blocks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PerMedCoE/permedcoe",
    author="PerMedCoE Project",
    author_email="infoPerMedCoE@bsc.es",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Science/Research",
        "Operating System :: Unix",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Environment :: Console",
    ],
    keywords="PerMedCoE",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6, <4",
    install_requires=["pyyaml"],
    extras_require={
        "dev": ["check-manifest"],
    },
    # If there are data files included in your packages that need to be
    # installed, specify them here.
    package_data={
        "permedcoe": ["templates/*",
                      "templates/application/*",
                      "templates/application/NextFlow/*",
                      "templates/application/PyCOMPSs/*",
                      "templates/application/SnakeMake/*",
                      "templates/building_block/*",
                      "templates/building_block/skeleton_BB/*",
                      "templates/building_block/skeleton_BB/container/*",
                      "templates/building_block/skeleton_BB/src/*",
                      "templates/building_block/skeleton_BB/src/bb/*",
                      "templates/building_block/skeleton_BB/src/bb/assets/*"],
    },
    entry_points={
        "console_scripts": [
            "permedcoe=permedcoe.__main__:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/PerMedCoE/permedcoe/issues",
        "Source": "https://github.com/PerMedCoE/permedcoe",
    },
)
