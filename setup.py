import pathlib
from setuptools import setup, find_packages

HERE: str = pathlib.Path(__file__).parent

setup(
    name='pyi18n-v2',
    version='1.2.1',
    description='Simple and easy to use internationalization'
                'library inspired by Ruby i18n',
    long_description=(HERE / "README.md").read_text(),
    long_description_content_type="text/markdown",
    author='Piotr Markiewicz',
    keywords=['pyi18n'],
    license='MIT License',
    author_email='sectasy0@gmail.com',
    url='https://github.com/sectasy0/pyi18n',
    packages=find_packages(),
    install_requires=['PyYAML>=6.0'],
    entry_points={
        'console_scripts': [
            'pyi18n-tasks=pyi18n.pyi18n_tasks:cli',
        ],
    },
)
