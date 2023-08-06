import setuptools

with open("README.md", "r") as fh:
    description = fh.read()

setuptools.setup(
    name="do-not-install-this-package",
    version="0.0.1",
    author="hackerman",
    author_email="hackerman@anotheruniverse.com",
    packages=["test_package"],
    description="A package you should not run on your device",
    long_description=description,
    long_description_content_tpye="text/markdown",
    url="",
    license="MIT",
    python_requires='>=3.8',
    install_requires=[]
)