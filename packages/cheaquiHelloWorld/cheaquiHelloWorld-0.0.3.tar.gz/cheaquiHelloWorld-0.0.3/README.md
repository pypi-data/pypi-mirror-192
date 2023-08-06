# Hello World

This is an example project demonstrating how to publish a python module to PyPI

## Installation

Run the following to install:

'''python
pip install cheaquiHelloWorld
'''

## Usage

'''python
from cheaquiHelloWorld import say_hello

# Generate "Hello, World!"
say_hello()

#Generate "Hello, Everybody!"
say_hellow("Everybody")
'''

# Developing Hello World

To install cheaquiHelloWorld, along with the tools you need to develop and run test, run the following in your virtualenv:


'''bash
$ pip install -e . [dev]
'''
