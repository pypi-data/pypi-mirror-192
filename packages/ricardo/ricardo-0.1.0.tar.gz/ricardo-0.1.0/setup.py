# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fabricius', 'fabricius.plugins', 'fabricius.plugins.define']

package_data = \
{'': ['*']}

install_requires = \
['chevron>=0.14.0,<0.15.0',
 'inflection>=0.5.1,<0.6.0',
 'rich>=12.4.4,<13.0.0',
 'typing-extensions>=4.2.0,<5.0.0']

extras_require = \
{'docs': ['Sphinx>=5.0.2,<6.0.0',
          'furo>=2022.6.21,<2023.0.0',
          'sphinx-autobuild>=2021.3.14,<2022.0.0']}

setup_kwargs = {
    'name': 'ricardo',
    'version': '0.1.0',
    'description': 'Fabricius: The supportive templating engine for Python!',
    'long_description': '# Fabricius\n\nFabricius - A Python 3.10 Project Template engine with superpowers!\n\n> :warning: Fabricius is a work in progress! Please, play with it with a grain of salt; expect bugs, crashes, non-documented portion of the application & more unexpected behavior.\n\nDocumentation: <https://fabricius.readthedocs.io>\n\n> :warning: Fabricius still does not comes with it\'s CLI tool! It is a work in progress!\n\n## Goals:\n\n1. Create a working project from a project template\n2. Create a fully working CLI using Rich\n3. Ability to clone repository and use their templates\n4. Create a secure tool (Do not allow unsecure scripts)\n5. Create a fully type hinted tool\n\n## Why the name of "Fabricius"?\n\nI am an immense fan of roman names, and I very often name my project after a meaningful roman name.\n\n"Fabricius" (In French, "Artisan") is translated to "craftsman", which is what Fabricius, the tool we create, aims to. His goal is to help at its best to create your projects easily.\n\n## Why not just use CookieCutter or Copier instead of creating your own tool?\n\nSee goals, but other than that,\n\nIt\'s a question I am expecting with fears, I tried to first use CookieCutter myself but I never liked it at all, it always broke with me and was painful to use. On top of that, it does not comes with crucial things I would personally require, such as basic type checking when gathering user\'s input.\nAs for Copier, while it seems like a much more grown-up tool and *actually* fitting my need, I honestly did not try it, I just lost interested towards it and wanted to challenge myself in creating a new tool for the Python ecosystem.\n\nOn top of all of these, during my work in 2022, I ended up using TypeScript and using AdonisJS\'s CLI tool, and its awesome [template generator](https://docs.adonisjs.com/guides/ace-commandline#templates-generator), and so it made me really interested into creating a project scaffolder but using code, not a directory structure, which was lacking for both tools.\n\nI wanted to create a complete and customizable experience of project scaffolding, I wanted to allow users to be free of do whatever they\'ve meant to do, it\'s how I came up with the idea of plugins.\n\nTo me, Fabricius is more than just a simple project scaffolder, it\'s a complete handy swiss knife for their users. :)\n',
    'author': 'Predeactor',
    'author_email': 'pro.julien.mauroy@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Predeactor/Fabricius',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
