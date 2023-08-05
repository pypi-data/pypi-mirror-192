from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'NMS Event Source'
LONG_DESCRIPTION = 'Event Source framework for creating a event store'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="event_source_srv", 
        version=VERSION,
        author="SonNM",
        author_email="<son20112074@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'event source'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
