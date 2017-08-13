from setuptools import setup, find_packages


setup(
    name='mlhoops',
    version='0.1',
    packages=find_packages(),
    description='A machine learning application for NCAA basketball',
    entry_points={
        'console_scripts': ['mlhoops=mlhoops.driver:main']
    }
)
