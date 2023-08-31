from distutils.core import setup

requirements = [
    "numpy",
    "matplotlib",
]

setup(
    author="Erik Hartman",
    author_email="erik.hartman@hotmail.com",
    name="polarda",
    version="0.0.1",
    packages=["polarda"],
    license="MIT",
    long_description=open("README.md").read(),
    install_requires=requirements,
)