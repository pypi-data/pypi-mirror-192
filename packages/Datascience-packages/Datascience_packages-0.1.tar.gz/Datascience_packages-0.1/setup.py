from setuptools import setup, find_packages

setup(
    name='Datascience_packages',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scipy',
        'scikit-learn',
        'matplotlib'
    ],
    entry_points='''
        [console_scripts]
        Datascience_packages=Datascience_packages.cli:main
    ''',
)