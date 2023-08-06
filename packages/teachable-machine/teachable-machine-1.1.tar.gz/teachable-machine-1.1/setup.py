from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent

VERSION = '1.1'
DESCRIPTION = 'A Python package to simplify the deployment process of exported Teachable Machine models into Python projects.'
LONG_DESCRIPTION = (this_directory / "README.md").read_text()

# Setting up
setup(
    name="teachable-machine",
    version=VERSION,
    author="Meqdad Dev (Meqdad Darwish)",
    author_email="meqdad.darweesh@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    py_modules=["teachable_machine", ],
    package_dir={"": "src"},
    install_requires=['numpy>=1.23.5',
                      'Pillow>=9.4.0',
                      'tensorflow>=2.12.0rc0'],
    url='https://github.com/MeqdadDev/teachable-machine',
    download_url='https://github.com/MeqdadDev/teachable-machine',
    keywords=['python', 'teachable machine', 'ai', 'computer vision',
              'camera', 'opencv', 'image classification'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ]
)
