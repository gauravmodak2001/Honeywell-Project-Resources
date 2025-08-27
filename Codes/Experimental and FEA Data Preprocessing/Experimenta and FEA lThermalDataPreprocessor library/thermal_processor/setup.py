from setuptools import setup, find_packages

setup(
    name="thermal_processor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.19.0",
        "pandas>=1.1.0",
        "matplotlib>=3.3.0",
        "scikit-image>=0.17.2",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A package for processing thermal image data",
    keywords="thermal, image, processing",
    url="https://github.com/yourusername/thermal_processor",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)