# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rotary_encoder_gpio_core']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rotary-encoder-gpio-core',
    'version': '0.1.0',
    'description': '',
    'long_description': '# rotary_encoder_gpio_core\n\nMeany only as a core dependency of `rotary-encoder`.\n\nThis is a fork of RPi.GPIO. For the original repo go to:\nhttp://sourceforge.net/p/raspberry-gpio-python/\n\n',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
