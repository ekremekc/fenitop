from setuptools import setup

setup(
    name='fenitop',
    version = '0.0.0',
    author='Ekrem Ekici',
    author_email='ekrem.ekici@kfupm.edu.sa',
    packages=['fenitop'],
    install_requires=[
        'pyvista',
        'scipy'
    ]
)
