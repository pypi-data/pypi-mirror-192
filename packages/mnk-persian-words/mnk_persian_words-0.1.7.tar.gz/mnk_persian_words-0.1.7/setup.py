from setuptools import find_packages, setup

setup(
    name='mnk_persian_words',
    packages=find_packages(include=['mnk_persian_words']),
    version='0.1.7',
    description='Creates REALLY random Persian words',
    author='Masoud Najafzadeh Kalat',
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",

)
