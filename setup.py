from setuptools import setup, find_packages

setup(
    name='sentiment-analysis-example',
    version='0.1',
    description='sentiment-analysis-example.',
    author='Piotr Malinski',
    author_email='riklaunim@gmail.com',
    url='https://github.com/riklaunim/sentiment-analysis-example',
    setup_requires=['pytest-runner'],
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
)
