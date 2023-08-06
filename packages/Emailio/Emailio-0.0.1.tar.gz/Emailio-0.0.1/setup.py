import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='Emailio',
    version='0.0.1',
    description='Emailio is a Python package that provides a simple and easy-to-use interface for sending emails with attachments. It uses the Simple Mail Transfer Protocol (SMTP) to send emails, and supports attachments of different file types.',
    author= 'Ravi shanker Lal',
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['Send email', 'Sendemail', 'Send email with attachments','Mail'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    py_modules=['Emailio'],
    package_dir={'':'src'},
    install_requires = [
    ]
)