import os

from setuptools import setup, find_packages
import sys

import subprocess as sp

if sys.version_info < (3, 7):
    print("This python version is not supported:")
    print(sys.version)
    print("Seq2Neo requires python 3.7 or greater")
    sys.exit(1)

data_files = []
for dirpath, dirnames, filenames in os.walk("seq2neo/function/immuno_Prediction/data"):
    for filename in filenames:
        data_files.append(os.path.join(os.path.relpath(dirpath, 'seq2neo/function/immuno_Prediction'), filename))

# 请提前装好conda
# 采用conda解决依赖问题
with open("requirement.txt", 'r') as f:
    req_packages = f.readlines()
req_packages = [req_package.strip() for req_package in req_packages]
req_packages_str = ' '.join(req_packages)

conda_cmd = "conda install -y " + req_packages_str
sp.check_call(conda_cmd, shell=True)

setup(
    name="Seq2Neo",
    version="v2.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'seq2neo.function.immuno_Prediction': data_files,
        '': ['requirement.txt'],
    },
    entry_points={
        "console_scripts": [
            "seq2neo = seq2neo.main:main",
        ]
    },
    author=" Kaixuan Diao",
    author_email="diaokx@shanghaitech.edu.cn",
    description="Seq2Neo: a comprehensive pipeline for cancer neoantigen immunogenicity prediction",
    keywords="neoantigen fusion immunogenicity prediction sequencing cancer",
    long_description_content_type="text/markdown",
    url="https://github.com/XSLiuLab/Seq2Neo",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Academic Free License (AFL)",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    python_requires='>=3'
)
