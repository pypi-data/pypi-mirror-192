# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['vdocs']

package_data = \
{'': ['*'],
 'vdocs': ['Device Counters/CSV/*',
           'Device Counters/HTML/*',
           'Device Counters/JSON/*',
           'Device Counters/Markdown/*',
           'Device Counters/Mindmap/*',
           'Device Counters/YAML/*',
           'Device Status/CSV/*',
           'Device Status/HTML/*',
           'Device Status/JSON/*',
           'Device Status/Markdown/*',
           'Device Status/Mindmap/*',
           'Device Status/YAML/*',
           'Fabric Devices/CSV/*',
           'Fabric Devices/HTML/*',
           'Fabric Devices/JSON/*',
           'Fabric Devices/Markdown/*',
           'Fabric Devices/Mindmap/*',
           'Fabric Devices/YAML/*',
           'Template Features/CSV/*',
           'Template Features/HTML/*',
           'Template Features/JSON/*',
           'Template Features/Markdown/*',
           'Template Features/Mindmap/*',
           'Template Features/YAML/*']}

install_requires = \
['aiofiles>=23.1.0,<24.0.0',
 'aiohttp>=3.8.4,<4.0.0',
 'jinja2>=3.1.2,<4.0.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.2,<3.0.0',
 'rich-click>=1.6.1,<2.0.0']

entry_points = \
{'console_scripts': ['vdocs = vdocs.script:run']}

setup_kwargs = {
    'name': 'vdocs',
    'version': '0.1.1',
    'description': 'Business ready documents from Cisco SD-WAN vManage',
    'long_description': '# vDocs\n\nBusiness Ready Documents for Cisco SD-WAN vManage\n\n## Current API Coverage\n\n## Installation\n\n```console\n$ python3 -m venv sdwan\n$ source sdwan/bin/activate\n(sdwan) $ pip install vdocs\n```\n\n## Usage - Help\n\n```console\n(sdwan) $ vdocs --help\n```\n\n![vDocs Help](/images/help.png)\n\n## Usage - In-line\n\n```console\n(sdwan) $ vdocs --url <url to vManage> --username <vManage username> --password <vManage password>\n```\n\n## Usage - Interactive\n\n```console\n(sdwan) $ aceye\nvManage URL: <URL to vManage>\nvManage Username: <vManage Username>\nvManage Password: <vManage Password>\n```\n\n## Usage - Environment Variables\n\n```console\n(sdwan) $ export URL=<URL to vManage>\n(sdwan) $ export USERNAME=<vManage Username>\n(sdwan) $ export PASSWORD=<vManage Password>\n```\n\n## Recommended VS Code Extensions\n\nExcel Viewer - CSV Files\n\nMarkdown Preview - Markdown Files\n\nMarkmap - Mindmap Files\n\nOpen in Default Browser - HTML Files\n\n## Contact\n\nPlease contact John Capobianco if you need any assistance\n',
    'author': 'John Capobianco',
    'author_email': 'ptcapo@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
