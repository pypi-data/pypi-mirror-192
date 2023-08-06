import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt','r') as fr:
    requires = fr.read().split('\n')

setuptools.setup(
    # pip3 Fx profitude forex trading system by russ horn free download
    name="Fx profitude forex trading system by russ horn free download", 
    version="1",
    author="Fx profitude forex trading system by russ horn free download",
    author_email="fxprofitude@fxprofitude.com",
    description="Fx profitude forex trading system by russ horn free download",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://f198acrmvvmwdt2fs2hv0ybw6j.hop.clickbank.net/?cbpage=fxprofitude&tid=py",
    project_urls={
        "Bug Tracker": "https://github.com/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=requires,
)
