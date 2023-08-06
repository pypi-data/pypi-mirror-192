# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['letnums']
install_requires = \
['pika>=0.0.1,<0.0.2']

setup_kwargs = {
    'name': 'letnums',
    'version': '0.0.2',
    'description': 'a simple library to generate random combinations of letters and numbers',
    'long_description': '## letnum\n\nletnum, a simple python library that is able to generate random letter and number combinations for you\n\nit is easy to use and only requires a 1 to 3 lines\n## Installation\n\npip install letnum\n\n```py\n#How to Use\nfrom letnum import number, letter, letter_number\n\n#u only need the function name\nnumber()\n#by typing the fuction name and running it will ask the amount of letters.\n"Enter Any Amount u want.."\n\n"(the same for every function {look at the photo})\n```\n\n## Screenshots\n\n![App Screenshot](https://cdn.discordapp.com/attachments/1076890796399276042/1076987830431137852/image.png)\n\n![App Screenshot](https://cdn.discordapp.com/attachments/1076890796399276042/1076987956256059432/image.png)\n\n',
    'author': 'Sokisa',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sokisa/letnum',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.11.1,<4.0.0',
}


setup(**setup_kwargs)
