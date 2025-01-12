from setuptools import setup

setup(
    name='fenitop',
    version = '0.0.0',
    author='Ekrem Ekici',
    author_email='ee331@cantab.ac.uk',
    packages=['fenitop'],
    install_requires=[
        'pyvista',
        'scipy'
    ]
)
