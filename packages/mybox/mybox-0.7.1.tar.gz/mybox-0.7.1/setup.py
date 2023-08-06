# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mybox', 'mybox.package', 'mybox.state']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'beautifulsoup4>=4.11.2,<5.0.0',
 'jsonpath-ng>=1.5.3,<2.0.0',
 'requests>=2.28.2,<3.0.0',
 'tqdm>=4.64.1,<5.0.0',
 'trio>=0.22.0,<0.23.0',
 'typed-argparse>=0.2.9,<0.3.0']

entry_points = \
{'console_scripts': ['mybox = mybox.main:sync_main']}

setup_kwargs = {
    'name': 'mybox',
    'version': '0.7.1',
    'description': 'Manage the configuration and tools on your workstation without bothering the OS too much',
    'long_description': '# Mybox\n\n🖥️ This is a box. 📦 And it is mine. 🐱\n\nThere are many 🍱 nice things in there. I wouldn\'t want 🧰 to be without them.\n\nEven if I move 🏠 or work 🏢 I want to be comfortable.\n\n---\n\nManage the configuration and tools on your workstation without bothering the OS\ntoo much (maybe your favorite one isn\'t supported by `$WORK` or you have\ndifferent ones for different roles).\n\n## Usage\n\n* Run the [bootstrap](bootstrap) script:\n\n  ```shell\n  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/koterpillar/mybox/main/bootstrap)"\n  ```\n\n* Run `mybox` from the directory with package definitions.\n\n  For package definition examples, see\n  [koterpillar/desktop](https://github.com/koterpillar/desktop/).\n\n* To install optional components, add their names as arguments, e.g.\n  `mybox development`.\n\n## Development\n\nPre-requisites (see [install-dev](install-dev) for ways to install):\n\n* [Poetry](https://python-poetry.org/)\n* [ShellCheck](https://www.shellcheck.net/)\n\nRun [`./lint`](lint) to check style & types, `./lint --format` to apply\nformatting automatically.\n\nRun [`./test`](test) to execute the project\'s tests.\n\n### Running locally\n\n* Run `poetry install`.\n* Run `poetry shell`.\n* In the launched shell, go to the directory with package definitions.\n* Run `mybox` with the desired arguments.\n\n### Releasing\n\nCreate and push a signed Git tag of the format `vX.Y.Z`. The release will be\ndone using GitHub actions.\n',
    'author': 'Alexey Kotlyarov',
    'author_email': 'a@koterpillar.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/koterpillar/mybox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
