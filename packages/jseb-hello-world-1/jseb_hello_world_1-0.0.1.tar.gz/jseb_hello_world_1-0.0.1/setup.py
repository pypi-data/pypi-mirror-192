from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'This is just a test'

# Setting up
setup(
    name="jseb_hello_world_1",
    version=VERSION,
    author="jsebdev",
    author_email="<jsebdev@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
