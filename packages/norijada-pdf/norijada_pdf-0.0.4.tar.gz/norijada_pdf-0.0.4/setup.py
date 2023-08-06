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
    'version': '0.0.4',
    'description': 'Utility for arranging short text in the PDF with minimum amount of empty space between text.',
    'long_description': '# Norijada PDF\n\nNorijada PDF is a Python library for generating PDF files from text files containing short text.\n\n\n## Installation\nCreate virtual environment and install norijada-pdf\n\n```bash\npip install norijada-pdf\n```\n\n## Usage\n\n1. List available fonts\n\n```bash\nnorijada-pdf list-fonts\n```\n\n2. Add new fonts\n\n```bash\nnorijada-pdf add-fonts\n```\n\nSpecify directory name other than fonts\n```bash\nnorijada-pdf add-fonts --dir some_dir\n```\n\n3. Generate PDF\n\nSettings will be automatically created in the current directory if it does not exist under settings.json file.\n\nExample settings.json file\n\n```json\n{\n    "font_sizes": {\n        "Bangers-Regular": 195,\n        "BebasNeue-Regular": 195,\n        "BerkshireSwash-Regular": 158,\n        "BlackOpsOne-Regular": 139,\n        "Bungee-Regular": 120,\n        "Courgette-Regular": 156,\n        "Galindo-Regular": 140,\n        "KaushanScript-Regular": 167,\n        "LibreBaskerville-Regular": 140,\n        "Lobster-Regular": 172,\n        "MouseMemoirs-Regular": 223,\n        "Pacifico-Regular": 147,\n        "PatrickHand-Regular": 190,\n        "Ranchers-Regular": 170,\n        "RubikMonoOne-Regular": 100,\n        "RussoOne-Regular": 140,\n        "SigmarOne-Regular": 110,\n        "Staatliches-Regular": 180,\n        "TitanOne-Regular": 130\n    },\n    "plot_increment": 1,\n    "page_width": 500,\n    "default_font_size": 150,\n    "max_length": 240\n}\n```\n\nYou can modify existing settings.json file or reset to defaults by running\n```bash\nnorijada-pdf reset-settings\n```\n\nPDF generator requires an input.txt file in the current directory. \nInput file should contain nicknames separated by new line. Additional arguments can be passed to the generator.\nRun help command to see all available arguments\n\n```bash\nnorijada-pdf generate-pdf --help\n```\n\nRun the PDF generator with the following command\n\n```bash\nnorijada-pdf generate-pdf --font BebasNeue-Regular.ttf\n```\n\nAdd unique id to the end of the file name\n\n```bash\nnorijada-pdf generate-pdf --font BebasNeue-Regular.ttf --file-id prhg-8a\n```\n\nExample input.txt file\n\n```text\nNetko Je Super Lik\nČižo\nŠtupid\nČakra\njajoslav\nKico\nPoki\nŠokac\nŠabo\njajan\nKošček\nČupavac\nVau\nKora\nĐuro\nPero\nStavros\nJasmin Stavros\nJasmin\nKalodont\n```\n\nExample output pdf file\n[nicknames-prhg-8a.pdf](example%2Fnicknames-prhg-8a.pdf)\n\nText can also be rotated to optimize the space on the page.\n\n```bash\nnorijada-pdf generate-pdf --font BebasNeue-Regular.ttf --file-id prhg-8a-rotated --rotate\n```\nExample output pdf file [nicknames-prhg-8a-rotated.pdf](example%2Fnicknames-prhg-8a-rotated.pdf)\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)',
    'author': 'marin',
    'author_email': 'marin.kruzic@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
