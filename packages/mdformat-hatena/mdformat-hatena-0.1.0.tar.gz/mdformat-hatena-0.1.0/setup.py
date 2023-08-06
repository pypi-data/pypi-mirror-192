from setuptools import find_packages, setup


setup(
    name="mdformat-hatena",
    version="0.1.0",
    packages=find_packages(),
    license="MIT",
    author="ZenProducts Inc.",
    description="mdformat for Hatena Blog markdown.",
    install_requires=[
        "mdformat>=0.7",
    ],
    entry_points={"mdformat.parser_extension": [
        "hatena = mdformat_hatena:plugin",
    ]}
)
