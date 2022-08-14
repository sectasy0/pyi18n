import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

setup(
    name='pyi18n-v2',
    version='1.0.1',
    description='Small and easy to use internationalization library inspired by Ruby i18n',
    long_description=(HERE / "README.md").read_text(),
    long_description_content_type="text/markdown",
    author='Piotr Markiewicz',
    keywords=['pyi18n'],
    license='MIT License',
    author_email='sectasy0@gmail.com',
    url='https://github.com/sectasy0/pyi18n',
    packages=find_packages(),
    install_requires=['PyYAML==5.3.1']
)