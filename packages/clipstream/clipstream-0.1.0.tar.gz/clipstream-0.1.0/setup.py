# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clipstream']

package_data = \
{'': ['*'],
 'clipstream': ['.mypy_cache/*',
                '.mypy_cache/3.10/*',
                '.mypy_cache/3.10/_typeshed/*',
                '.mypy_cache/3.10/asyncio/*',
                '.mypy_cache/3.10/clipstream/*',
                '.mypy_cache/3.10/collections/*',
                '.mypy_cache/3.10/concurrent/*',
                '.mypy_cache/3.10/concurrent/futures/*',
                '.mypy_cache/3.10/ctypes/*',
                '.mypy_cache/3.10/email/*',
                '.mypy_cache/3.10/importlib/*',
                '.mypy_cache/3.10/importlib/metadata/*',
                '.mypy_cache/3.10/logging/*',
                '.mypy_cache/3.10/multiprocessing/*',
                '.mypy_cache/3.10/os/*']}

install_requires = \
['asynkets>=0.1.0,<0.2.0', 'pyperclip>=1.8.2,<2.0.0', 'python-xlib>=0.33,<0.34']

entry_points = \
{'console_scripts': ['clipstream = clipstream.__main__:clipstream_to_stdout']}

setup_kwargs = {
    'name': 'clipstream',
    'version': '0.1.0',
    'description': '',
    'long_description': "# Clipstream\n\nClipstream is a tool for printing clipboard contents to the standard output as they change. It provides a convenient way to access the system clipboard from the command line. \n\nOn a Linux system with X and the XFIXES extension, `clipstream` receives clipboard updates without creating processes constantly for polling.\n\n## Installation\n\nClipstream can be installed with pip:\n\n```\npip install clipstream\n```\n\nFor use as a command-line tool, it is recommended to use `pipx` to install Clipstream in its own isolated environment:\n\n```\npipx install clipstream\n```\n\n## Usage as a Command-Line Tool\n\nClipstream can be run from the command line with the following command:\n\n```\nclipstream\n```\n\nThis will print the current contents of the clipboard to the standard output as they change.\n\nThere are several options available for customizing the output of Clipstream:\n\n```\n-n, --newline        Print a newline after each clipboard item.\n-1, --one            Print one clipboard item, then exit.\n-i, --include-initial Include the initial clipboard item.\n-s, --strip           Strip whitespace from clipboard items.\n-r, --polling-rate    How often to poll the clipboard, in Hz (times per second).\n-0, --null            Print a null byte after each clipboard item.\n-u, --unique          Print only unique clipboard items.\n```\n\n## Usage as a Library\n\nClipstream can also be used as a library in Python projects. To use Clipstream as a library, simply import the `clipboard_stream` function from the `clipstream.stream` module:\n\n```python\nfrom clipstream.stream import clipboard_stream\n```\n\nThe `clipboard_stream` function returns an asynchronous generator that yields the contents of the clipboard as they change.\n\n## Examples\n\nHere are some examples of how Clipstream can be useful as a tool:\n\n- Downloading files from copied links:\n\n```bash\nclipstream | xargs -I_ wget _\n```\n\n- Writing copied text to a file:\n\n```bash\nclipstream | tee -a copied_text_file\n```\n\n- Get clipboard history + selector with a preview:\n\n```bash\nclipstream --strip --unique -0 | fzf --read0 --preview 'echo -n {}' --bind 'enter:execute(echo {} | xclip -selection clipboard)'\n```\n",
    'author': 'Pedro Batista',
    'author_email': 'pedrovhb@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
