# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonlf']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.14.0,<3.0.0']

entry_points = \
{'console_scripts': ['gstui = jsonlf.main:main']}

setup_kwargs = {
    'name': 'jsonlf',
    'version': '0.1.0',
    'description': 'Pretty print a stream of json lines. You can pipe any command that is logging jsonl into this. If the line is not a json it will print as it is.',
    'long_description': '# jsonlf\n\nThis is a json line formarter. It expects a valid json on stdin and outputs it pretty-printed and uses [pygments](https://pygments.org) for highlighting. It will also attempt to format python tracebacks.\n\n## Installation\n\n```sh\npip install jsonlf\n```\n\n## Usage\n\n```sh\nsome_command_that_logs_json_lines | jsonlf\n```\n\nYou can use pygments styles listed here: https://pygments.org/styles/\nJust pass their names as the first argument. Example:\n\n\n```sh\nsome_command_that_logs_json_lines | jsonlf emacs\n```\n',
    'author': 'Matheus Fillipe',
    'author_email': 'matheusfillipeag@gmail.com',
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
