from setuptools import setup

readme = open('./README.md', 'r')

setup(
    name='bayesian_network_clb',
    packages=['bayesian_network_cl'],
    version='0.1',
    description='Bayesian Network...',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author='Cris LB',
    author_email='cristianlaynezbachez@gmail.com',
    url='https://github.com/CRLB-sketch/AI_Lab2',
    download_url='https://github.com/CRLB-sketch/AI_Lab2/tarball/0.1',
    keywords=['exercise', 'testing', 'prototype'],
    classifiers=[],
    license='MIT',
    include_package_data=True,
)