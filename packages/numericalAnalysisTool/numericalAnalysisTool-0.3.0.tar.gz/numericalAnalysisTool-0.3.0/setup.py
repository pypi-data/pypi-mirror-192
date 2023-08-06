import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="numericalAnalysisTool",
    version="0.3.0",
    author="Clément Dutriez",
    author_email="clement.dutriez@u-pem.fr",
    description="Numerical anlysis tool kit",
    url="https://github.com/CafeKrem/pyNumericalAnlysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'pandas',
        'numpy',
        'seaborn',
        'plotly'
    ]

)
