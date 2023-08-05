from setuptools import setup

setup(
    name='lzmodelndata',
    version='0.1',
    description='model data package',
    author='lz',
    author_email='jhs012@gmail.com',
    packages=['lzpackage'],
    install_requires=[
        'numpy',
        'pandas'
    ]
)
