import setuptools

with open("../README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="a3py",
    version="0.0.1",
    author="Abe Davis", # you can change this to you
    author_email="yourID@cornell.edu",
    description="my a3py code ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.coecis.cornell.edu/CS6682-Spring2021/a3_audio/",
    project_urls={
        'My webpage': 'yourwebpage.com',
        'Source': 'https://github.coecis.cornell.edu/-------',
    },
    install_requires=[
        'numpy',
        'scipy',
        'jsonpickle',
        'mido',
        'librosa',
        'matplotlib',
        'future',
        'six',
        'termcolor',
        'apy',
        'ipywidgets',
        'drawSvg',
    ],
    packages=setuptools.find_packages(exclude=['contrib', 'docs', 'tests*']),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    zip_safe=False,
)
