from setuptools import setup, find_packages

setup(
    name='calculator_2023_02_15',
    version='0.1.1',
    author='Rapolas Strazdas',
    author_email='rmstrazdas@outlook.com',
    description='An extraordinarily basic calculator package',
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)