import setuptools
from setuptools import setup
from pathlib import Path

setuptools.setup(
    name='jxh_env',
    version='0.0.1',
    description="A OpenAI Gym Env for jxh",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include="jxh_env*"),
	install_requires=['gym']
)
