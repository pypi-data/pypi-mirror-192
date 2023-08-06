from setuptools import setup

setup(
    name='gensarpy',
    version='0.1.0',
    description='A program that includes different tests, distinguishes series as convergent or divergent',
    packages=['gensarpy'],
    install_requires=[
        'sympy'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)