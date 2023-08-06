import setuptools

setuptools.setup(
    name="aivisiontools",
    version="0.0.1",
    author="Eduard Cojocea",
    description="This package contains useful tools for Compute Vision practitioners for processing images, evaluating"
                "models etc. It is a package meant as a complementary to other more complex packages such as"
                "tensorflow, pytorch, opencv. It is not meant to compete or replace such packages, but rather"
                "to offer such tools which a developer needs to use those packages without writing himself many "
                "helper functions.",
    packages=["aivisiontools"]
)