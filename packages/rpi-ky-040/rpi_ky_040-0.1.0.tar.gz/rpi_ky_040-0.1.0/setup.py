# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rpi_ky_040']

package_data = \
{'': ['*']}

extras_require = \
{':platform_machine == "aarch64"': ['rpi-gpio>=0.7.1,<0.8.0']}

setup_kwargs = {
    'name': 'rpi-ky-040',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
