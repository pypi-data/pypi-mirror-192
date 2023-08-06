from setuptools import setup
from pathlib import Path


# Version number
with open("gtfsutils/__init__.py") as f:
    for line in f:
        if "__version__" in line:
            version = line.split("=")[1].strip().strip('"').strip("'")
            continue

# The text of the README file
this_directory = Path(__file__).absolute().parent
with open(this_directory / "README.md") as f:
    README = f.read()

# Requirements
try:
    this_directory = Path(__file__).absolute().parent
    with open((this_directory / 'requirements.txt'), encoding='utf-8') as f:
        requirements = f.readlines()
    requirements = [line.strip() for line in requirements]
except FileNotFoundError:
    requirements = []

setup(
    name='gtfsutils',
    version=version,
    url='https://github.com/triply-at/gtfsutils',
    author='Nikolai Janakiev',
    author_email='n.janakiev@triply.at',
    description='GTFS command-line tool and Python GTFS utility library',
    long_description=README,
    long_description_content_type='text/markdown',
    license="MIT",
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    platforms='any',
    packages=['gtfsutils'],
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "gtfsutils = gtfsutils.__main__:main"
        ]
    }
)
