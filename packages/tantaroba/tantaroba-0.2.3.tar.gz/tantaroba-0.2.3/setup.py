import setuptools

from tantaroba.__version__ import __version__

# You may want to only use pyproject.toml for building and publishing the package.
# So that semanti-release is only use to update the version, poetry does all the other stuff.

setuptools.setup(
    name="tantaroba",
    version=__version__,
    author="Mattia Tantardini",
    author_email="mattia.tantardini@gmail.com",
    description="Collection of miscellanoeus utilities commonly used across different projects",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.10,<4.0",
    install_requires=["psycopg2", "sqlalchemy", "pandas", "numpy", "loguru"],
)
