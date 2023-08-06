# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinx_prompt']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['Sphinx>=6.0.0,<7.0.0', 'docutils', 'pygments']

setup_kwargs = {
    'name': 'sphinx-prompt',
    'version': '1.6.0',
    'description': 'Sphinx directive to add unselectable prompt',
    'long_description': "Sphinx Prompt\n=============\n\n.. contents:: Table of contents\n\nInitialize\n----------\n\nIn ``conf.py`` add ``extensions += ['sphinx-prompt']``.\n\nSyntax\n------\n\nA default prompt can be created using a ``prompt`` directive:\n\n.. code::\n\n    .. prompt::\n\n       <statements>\n\nThe prompt can be further customized in one of two ways:\n\n- Using positional arguments:\n\n    .. code::\n\n        .. prompt:: [<language> [<prompts> [<modifiers>]]]\n\n           <statements>\n\n- Using options:\n\n    .. code::\n\n        .. prompt::\n            :language: <language>\n            :prompts: <prompts>\n            :modifiers: <modifiers>\n\n           <statements>\n\nWhile these constructs generate the same output, the positional arguments cannot be used\nif you want to use a prompt that contains spaces. This is a limitation of reStructuredText.\n\nPositional arguments can be mixed with options **if** they don't overlap\n(so if you pass prompts using options, you can only pass the language using positional arguments):\n\n.. code::\n\n    .. prompt:: bash\n        :prompts: (cool_project) $\n\n       python3 -m pip install --upgrade sphinx-prompt\n\nLanguage\n~~~~~~~~\n\nSupported language:\n\n- ``text`` (no pigments, default)\n- ``bash``\n- ``batch``\n- ``powershell``\n- ``python``\n- ``scala``\n\nPrompt(s)\n~~~~~~~~~\n\nIf modifier is auto, a comma-separated list of prompts to find in the statements.\n\nElse the prompt to add on each statements, for Python and Bash language the end\n``\\`` is supported.\n\nDefaults to empty, except for the shell languages listed below:\n\n- ``bash`` - ``$``\n- ``batch`` - ``C:\\>``\n- ``powershell`` - ``PS C:\\>``\n\nExamples\n--------\n\nSee: http://sbrunner.github.io/sphinx-prompt/\n\nRun tests and prospector\n------------------------\n\n.. code::\n\n    python3 -m pip install --user --upgrade poetry\n    poetry install\n    poetry run pytest\n    poetry run prospector\n\nThe code should be formatted with ``black`` add ``isort``.\n\nCreate new release\n------------------\n\n.. code::\n\n    git tag <version>\n    git push origin <version>\n",
    'author': 'Stéphane Brunner',
    'author_email': 'stephane.brunner@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://hub.docker.com/r/sbrunner/sphinx-prompt/',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
