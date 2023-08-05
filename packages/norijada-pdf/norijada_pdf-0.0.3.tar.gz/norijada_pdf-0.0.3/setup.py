# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['norijada_pdf']

package_data = \
{'': ['*'], 'norijada_pdf': ['fonts/*']}

install_requires = \
['fpdf2>=2.6.1,<3.0.0', 'rectpack>=0.2.2,<0.3.0']

entry_points = \
{'console_scripts': ['norijada-pdf = norijada_pdf:parse_cli']}

setup_kwargs = {
    'name': 'norijada-pdf',
    'version': '0.0.3',
    'description': 'Utility for arranging short text in the PDF with minimum amount of empty space between text.',
    'long_description': '# Norijada PDF\n\nNorijada PDF is a Python library for generating PDF files from text files containing nicknames.\n\n\n## Installation\n\nUse the package manager [Poetry](https://python-poetry.org/docs/#installation).\n\n```bash\npoetry install\n```\n\n## Usage\n\nAvailable fonts can be seen in the [fonts](fonts) directory and new fonts can be added as long \nthey are in .ttf format.\n\n```bash\n\n```\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first\nto discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)',
    'author': 'marin',
    'author_email': 'marin.kruzic@gmail.com',
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
