#!/usr/bin/env python

import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
        name='cuescience-payment',
        version='0.1',
        description='Payment modules for cuescience shop',
        maintainer='cuescience',
        maintainer_email='kontakt@cuescience.de',
        license="-",
        url='',
        packages=['payment', 'payment.services', 'payment.services.paypal'],
        install_requires=[
	    "Django",
	    "paypalrestsdk",
	]
     )
