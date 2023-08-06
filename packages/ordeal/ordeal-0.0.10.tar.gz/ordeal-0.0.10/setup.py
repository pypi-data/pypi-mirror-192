# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ord']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0',
 'httpx>=0.23.3,<0.24.0',
 'pydantic>=1.10.0,<2.0.0']

setup_kwargs = {
    'name': 'ordeal',
    'version': '0.0.10',
    'description': 'bitcoin jpegs',
    'long_description': '[![pypi](https://img.shields.io/pypi/v/ordeal.svg)](https://pypi.python.org/pypi/ordeal)\n\nA sandbox for working with [ord](https://github.com/casey/ord): `pip install ordeal`\n\nFor now, api calls go through https://ordapi.xyz/ but an [official api is in the works](https://github.com/casey/ord/pull/1662). Will switch to that once available, or start wrapping the ord crate from python.\n\n## Setup\n\nClone, `poetry install` then `pre-commit install`.\n\n`poetry run pytest`\n\n\n## Usage\n\nAll subject to change. Just exploring the api for now.\n\nA simple example of iterating through inscriptions and printing any with plaintext content:\n\n```python\nfrom ord import client\n\nfor i, inscription_id in client.inscriptions(start=0, stop=100):\n    inscription = client.get_content(inscription_id)\n    try:\n        plaintext = inscription.decode("utf-8")\n        print(i, inscription_id, "plaintext content")\n        print(plaintext, "\\n\\n")\n    except UnicodeDecodeError:\n        pass\n```\n',
    'author': 'Sam Barnes',
    'author_email': 'sam.barnes@opensea.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
