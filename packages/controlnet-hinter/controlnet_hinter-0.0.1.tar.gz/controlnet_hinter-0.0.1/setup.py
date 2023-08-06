import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

def _requires_from_file(filename):
    return open(filename).read().splitlines()

setuptools.setup(
    name="controlnet_hinter",
    version="0.0.1",
    author="takuma104",
    author_email="takuma104@gmail.com",
    description="ControlNet hint embedding utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/takuma104/controlnet_hinter",
    py_modules=['controlnet_hinter', 'annotator'],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=_requires_from_file('requirements.txt'),
)