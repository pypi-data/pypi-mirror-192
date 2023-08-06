from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Neural Network Logic Operators'
LONG_DESCRIPTION = 'Python package to perform operations using logical operators (AND, OR, NAND, NOR, NOT), but the operation is performed by neural networks.'

setup(
    name="neuralnetlogical",
    author="Eduardo Weber Maldaner",
    author_email="eduwmaldaner@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'matplotlib'],
    keywords=['python', 'python3', 'neural networks', 'neural nets', 'logical operators', 'neural net logical operators'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
    ]
)