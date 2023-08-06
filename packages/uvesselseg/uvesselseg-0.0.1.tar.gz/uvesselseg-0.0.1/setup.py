from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'U-net for vessel segmentation'
LONG_DESCRIPTION = 'U-net for vessel segmentation on large tif for spinal cord microscopy images of mice'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="uvesselseg", 
        version=VERSION,
        author="Olivier Tastet",
        author_email="o.tastet33@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['torch',
                          'opencv-python',
                          'natsort',
                          'sklearn',
                          'patchify',
                          'tqdm',
                          'scipy',
                          'pandas',
                          'albumentations',
                          'pillow',
                          'numpy',
                          'argparse',
                          'matplotlib',
                          'torchvision'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'vessel segmentation'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)