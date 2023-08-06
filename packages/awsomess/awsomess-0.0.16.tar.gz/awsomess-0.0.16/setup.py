from setuptools import setup
from setuptools import find_packages

setup(
    name="awsomess",
    version="0.0.16",
    description="just to test deployment and nothing else",
    long_description="here is a long description of this project",
    author="afonso",
    author_email="a.schulzalbrecht@gmail.com",
    # package_dir={"": "src"},  # allows: import awsomess
    packages=find_packages(exclude=("group*")),
)
