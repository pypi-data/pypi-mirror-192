from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='aircraft_list',
    version='2.2',
    description='This package contains a list of the Aircraft models and manufacturer as per DOC 8643 ICAO',
    author='Giorgio Scarso',
    author_email='scarso.giorgio@gmail.com',
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['pandas'],
    url='https://github.com/George88000/aircraft_models',
    package_data={'aircraft_list': ['aircraft_model_list.csv']},
)