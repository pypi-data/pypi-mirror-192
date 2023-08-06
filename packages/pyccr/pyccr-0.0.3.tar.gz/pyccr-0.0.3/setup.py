from setuptools import setup

setup(
    name='pyccr',
    version='0.0.3',
    description='Contextualized Construct Representations (CCR).',
    long_description='',
    url='https://github.com/Ali-Omrani',
    author='Ali Omrani',
    author_email='aomrani@usc.edu',
    packages=["ccr"],
    classifiers=['Development Status :: 1 - Planning'],
    install_requires =['pandas', 'numpy', 'sentence_transformers']
)