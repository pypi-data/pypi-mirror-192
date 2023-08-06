# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['glue_biscuit', 'glue_biscuit.test']

package_data = \
{'': ['*']}

install_requires = \
['black==22.3.0',
 'boto3==1.21.29',
 'botocore==1.24.46',
 'cfn-flip==1.3.0',
 'click==8.1.3',
 'jmespath==1.0.1',
 'mypy-extensions==0.4.3',
 'pathspec==0.10.1',
 'platformdirs==2.5.2',
 'python-dateutil==2.8.2',
 's3transfer==0.5.2',
 'six==1.16.0',
 'tomli==2.0.1',
 'typing-extensions==4.3.0',
 'urllib3==1.26.12']

setup_kwargs = {
    'name': 'glue-biscuit',
    'version': '0.0.2',
    'description': '',
    'long_description': '### Setup for local development (installing dependencies for IDE highlighting)\n\n1. Clone Repo\n1. Install Python 3.7\n   - Newer versions of Python 3 will probably work, but won\'t match the PyGlue\n1. Download [PyGlue.zip](https://s3.amazonaws.com/aws-glue-jes-prod-us-east-1-assets/etl-1.0/python/PyGlue.zip)\n   - Documentation around this can be found [here](https://docs.aws.amazon.com/glue/latest/dg/dev-endpoint-tutorial-pycharm.html)\n   - Put this zip in the project directory after cloning locally\n1. Install dependencies `pip install -r requirements.txt`\n1. (If using VSCode) Create `.env` in the project directory\n   - Add a line adding the PyGlue.zip file to your PYTHONPATH environment variable. e.g. `PYTHONPATH=".:/Users/bskiff/projects/python-stuff/GlueTest/PyGlue.zip"`\n\n### Running tests\n\n1. Install Docker\n1. Run `docker build -t glue . && docker run -it glue`\n\n### Linting and formatting\n\n```bash\nmake lint # checks linting and styles\nmake format # fixes style rule violations\n```\n',
    'author': 'Gene Tinderholm',
    'author_email': 'gtinderholm@sourceallies.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
