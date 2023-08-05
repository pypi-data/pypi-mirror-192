from setuptools import setup

setup(
    name='lzmysample',
    version='0.1',
    description='My Python package',
    author='lz',
    author_email='jhs012@gmail.com',
    packages=['lzpackage'],
    install_requires=[
        'numpy',
        'pandas'
    ]
)
