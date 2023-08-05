# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oracle_of_ammon',
 'oracle_of_ammon.api',
 'oracle_of_ammon.api.utils',
 'oracle_of_ammon.cli',
 'oracle_of_ammon.locust',
 'oracle_of_ammon.tests',
 'oracle_of_ammon.utils']

package_data = \
{'': ['*'], 'oracle_of_ammon': ['data/*']}

install_requires = \
['aiofiles>=22.1.0,<23.0.0',
 'bs4>=0.0.1,<0.0.2',
 'farm-haystack>=1.13.0,<2.0.0',
 'fastapi>=0.88.0,<0.89.0',
 'locust>=2.14.0,<3.0.0',
 'markdown>=3.2.1,<3.4',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.5.2,<2.0.0',
 'pdf2image>=1.16.2,<2.0.0',
 'psutil>=5.9.4,<6.0.0',
 'pynvml>=11.4.1,<12.0.0',
 'pytesseract>=0.3.10,<0.4.0',
 'python-frontmatter>=1.0.0,<2.0.0',
 'python-magic>=0.4.27,<0.5.0',
 'python-multipart>=0.0.5,<0.0.6',
 'requests>=2.28.1,<3.0.0',
 'typer[all]>=0.7.0,<0.8.0',
 'types-psutil>=5.9.5.6,<6.0.0.0',
 'uvicorn>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['oracle-of-ammon = oracle_of_ammon.cli.main:app']}

setup_kwargs = {
    'name': 'oracle-of-ammon',
    'version': '0.3.2',
    'description': 'CLI tool for creating Search APIs.',
    'long_description': "# Oracle of Ammon\n\n[![PyPI version shield](https://img.shields.io/pypi/v/oracle-of-ammon?color=blue&style=flat-square)](https://pypi.org/project/oracle-of-ammon/)\n[![Python version shield](https://img.shields.io/pypi/pyversions/oracle-of-ammon?color=blue&style=flat-square)](https://pypi.org/project/oracle-of-ammon/)\n[![MIT License](https://img.shields.io/github/license/kmcleste/oracle-of-ammon?style=flat-square)](https://github.com/kmcleste/oracle-of-ammon/blob/main/LICENSE)\n\nA simple CLI tool for creating Search APIs.\n\n## Installation\n\nCreating a virtual environment is highly recommended. To do so, run:\n\n```bash\npython3 -m venv .venv\nsource .venv/bin/activate\n```\n\nOnce your environment is active, simply install the package with:\n\n```bash\npip install oracle-of-ammon\n```\n\n## Usage\n\nTo get started, checkout the help menu:\n\n```bash\noracle-of-ammon --help\n```\n\n[![Image of oracle-of-ammon cli help documentaiton](https://github.com/kmcleste/oracle-of-ammon/blob/main/images/oracle-of-ammon-help.gif?raw=true)](https://github.com/faressoft/terminalizer)\n\nHere, you will see we currently have two options: **summon** and **locust**.\n\n### Summon\n\nBy default, Summon is configured to initialize an empty search service on port 8000. The API framework used is [FastAPI](https://fastapi.tiangolo.com/) and the underlying search engine is built on [Haystack](https://docs.haystack.deepset.ai/). If you would like to initialize the search service with documents upon startup, provide a filepath with the `--path` option. Once the service has been initialized, you can view the API docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). A static version of the swagger documentation can also be found [here](https://petstore.swagger.io/?url=https://raw.githubusercontent.com/kmcleste/oracle-of-ammon/main/openapi.json#/).\n\n| Option        | Type | Default         | Description                                                                                                                         |\n| ------------- | ---- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------- |\n| --path        | TEXT | None            | Filepath used to pre-index document store.                                                                                          |\n| --sheet-name  | TEXT | None            | If using an excel file, select which sheet(s) to load. If none provided, all sheets will be loaded. Expects a comma-separated list. |\n| --title       | TEXT | Oracle of Ammon | API documentation title.                                                                                                            |\n| --index       | TEXT | document        | Default index name.                                                                                                                 |\n| --faq         | BOOL | TRUE            | Selector for content preloaded into document store.                                                                                 |\n\nSupported Filetypes:\n\n- FAQ: CSV, TSV, JSON, XLSX, TXT\n- Semantic: TXT\n\nSee the [`data`](https://github.com/kmcleste/oracle-of-ammon/tree/main/oracle_of_ammon/data) directory for examples of accepted files.\n\n[![Oracle of Ammon CLI - Summon](https://github.com/kmcleste/oracle-of-ammon/blob/main/images/oracle-of-ammon-summon.gif?raw=true)](https://github.com/faressoft/terminalizer)\n\n### Locust\n\n[Locust](https://locust.io/) is an open source tool for load testing. You're able to swarm your system with millions of simultaneous users -- recording service performance and other metrics. By default, Locust will start on port 8089. To start a new load test, simply enter the number of users you want to simulate, their spawn rate, and the host address to swarm.\n\n[![Image of locust config](https://github.com/kmcleste/oracle-of-ammon/blob/main/images/locust-config.png?raw=true)](https://locust.io)]\n\n## Coming Eventually 👀\n\n- ~~Semantic search~~\n- ~~Document search~~\n- ~~Document summarization~~\n- Document ranking\n- ~~Multiple index support~~\n- Annotations/Feedback\n- Fine tuning\n- Additional locust endpoints\n- Dynamic Locust config\n- Custom pipelines\n- Dedicated docs wiki\n",
    'author': 'Kyle McLester',
    'author_email': 'kyle.mclester@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://kmcleste.github.io/oracle-of-ammon/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<3.11',
}


setup(**setup_kwargs)
