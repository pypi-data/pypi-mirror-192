# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['paper2txt']

package_data = \
{'': ['*']}

install_requires = \
['pdfminer']

entry_points = \
{'console_scripts': ['paper2txt = paper2txt.executable:paper2txt_main']}

setup_kwargs = {
    'name': 'paper2txt',
    'version': '0.0.2',
    'description': 'Simple tool to extract text from scientific PDFs',
    'long_description': '# paper2pdf\n\nA minimalist tool to extract text from modern PDFs (no OCR). \n\n```\npaper2txt myPDF.pdf outputfile.txt\n```\n\n',
    'author': 'Reto Stamm',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/retospect/paper2txt',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
