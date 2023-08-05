from setuptools import setup, find_packages

setup(
    name='aircraft_list',
    version='1.8',
    description='This package contains a list of the Aircraft models and manufacturer as per DOC 8643 ICAO',
    author='Giorgio Scarso',
    author_email='scarso.giorgio@gmail.com',
    packages=find_packages(),
    install_requires=['pandas'],
    url='https://github.com/George88000/aircraft_models',
    package_data={'aircraft_list': ['aircraft_model_list.csv']},
)