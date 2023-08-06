# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['git_command']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'git-command',
    'version': '0.0.1',
    'description': 'A simple interface to the Git command-line tools for Python.',
    'long_description': '# git-command\n\nA simple interface to the [Git][1] command-line tools for Python.\n\n## License\n\nCopyright (C) 2022 HE Yaowen <he.yaowen@hotmail.com>\n\nThe GNU General Public License (GPL) version 3, see [LICENSE](./LICENSE).\n\n[1]: https://git-scm.com/\n',
    'author': 'HE Yaowen',
    'author_email': 'he.yaowen@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
