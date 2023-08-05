from setuptools import find_packages, setup

setup(
    name="arve",
    version="0.1.2",
    description="Analyzing Radial Velocity Elements",
    url="https://github.com/almoulla/arve",
    author="Khaled Al Moulla",
    author_email="khaled.almoulla@gmail.com",
    license="MIT License",
    packages=find_packages(),
    install_requires=["astroquery",
                      "lmfit"     ,
                      "matplotlib",
                      "numba"     ,
                      "numpy"     ,
                      "scipy"
                     ],

    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    include_package_data=True,
    package_data={"arve": ["aux_data/masks/*.mask"]}
)