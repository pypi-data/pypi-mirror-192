from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name='mikeracingf1',
    version='0.0.4',
    author='Michele Berardi',
    author_email='michymak@gmail.com',
    url='https://github.com/micheleberardi/mikeracingf1',
    packages=find_packages(),
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description= 'A package for get Formula One Data',
    long_description=long_description,
    long_description_content_type="text/markdown",
)