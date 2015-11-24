from setuptools import setup, find_packages
import sys

INSTALL_REQUIRES = []

if sys.version_info < (3, 5):
    INSTALL_REQUIRES.append('pytracemalloc')


setup(
    name='puma',
    version='0.1.0',
    packages=find_packages(),
    url='https://github.com/gisce/puma',
    license='MIT',
    install_requires=INSTALL_REQUIRES,
    author='GISCE-TI, S.L.',
    author_email='devel@gisce.net',
    description='Use python tracemalloc to send snapshots to tracemalloc server.'
)
