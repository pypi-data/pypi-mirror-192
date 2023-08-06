from setuptools import setup, find_packages

setup(
    name='maphis', 
    packages=find_packages(exclude=['maphis.bin']),
    include_package_data=True,
    exclude_package_data={'': ["*.pt", "Tesseract-OCR/*"]},
    setup_requires=['setuptools_scm'],
    install_requires=[
        "appdirs",
        "numpy~=1.19.5",
        "scikit-image~=0.19.0",
        "PySide6",
        "opencv-python~=4.2.0.34",
        "ExifRead~=2.3.2",
        "Pillow~=8.4.0",
        "imagecodecs",
        "numba~=0.55.1",
        "openpyxl~=3.0.9",
        "scikit-learn~=1.0.2",
        "scipy~=1.8.0",
        "pytesseract~=0.3.9",
        "mouse",
        "torch",
        "arthseg",
        "pyparsing",
        "requests"
    ])
