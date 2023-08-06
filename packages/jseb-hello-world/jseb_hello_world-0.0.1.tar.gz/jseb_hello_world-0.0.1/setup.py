from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'This is just a test'
LONG_DESCRIPTION = 'there is no long description'

# Setting up
setup(
    name="jseb_hello_world",
    version=VERSION,
    author="jsebdev",
    author_email="<jsebdev@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
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
