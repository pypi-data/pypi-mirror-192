from pathlib import Path
from setuptools import setup, find_packages

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '1.0.0'
DESCRIPTION = 'A Library for the nosytx.eu Image API'

setup(
    name="nosytx",
    version=VERSION,
    author="Erik05Master",
    author_email="<info@sytxlabs.eu>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['aiohttp'],
    keywords=['python', 'api']
)