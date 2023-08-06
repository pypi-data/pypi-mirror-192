# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eromedownloader']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles', 'aiohttp', 'beautifulsoup4', 'requests', 'tqdm']

setup_kwargs = {
    'name': 'eromedownloader',
    'version': '0.0.1',
    'description': 'A Downloader for erome.com',
    'long_description': '# eromedownloader\n\n__Downloader for erome.com hosted as python package installable via pip__\n\n## Installation\n\n```shell\npip install eromedownloader\n```\n\n## Basic Usage\n\n```shell\npython eromedownloader --url https://www.erome.com/a/{ALBUM_ID}  \n```\n\n## Optional Arguments\n\n- *--path*: str, path/to/save/dir\n- *--override*: bool, whether to override album if already exists instead of downloading it under an incremented name version; __Default=False__\n- *--concurrent-requests-max*: int, max number of requests to be sent; sending too many requests at once may comprise the risk of getting your IP banned by erome; __Default=4__\n- *--ignore-images*: bool; __Default=False__\n- *--ignore-videos*: bool; __Default=False__',
    'author': 'masteroftheskies',
    'author_email': 'masteroftheskies@proton.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/masteroftheskies/eromedownloader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
