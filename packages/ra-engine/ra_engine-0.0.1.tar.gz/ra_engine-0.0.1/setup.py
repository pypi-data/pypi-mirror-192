from setuptools import setup, find_packages

setup(
    name="ra_engine",
    version="0.0.1",
    license="MIT",
    author="Navindu Dananaga",
    author_email="navindudananga123@gmail.com",
    packages=find_packages("src"),
    package_dir={"": "ra_engine"},
    url="https://github.com/SLTDigitalLab/RAE-sdk-python.git",
    keywords="ra_engine",
    long_description="""RAE SDK for Python""",
    install_requires=[
        "requests",
    ],
)
