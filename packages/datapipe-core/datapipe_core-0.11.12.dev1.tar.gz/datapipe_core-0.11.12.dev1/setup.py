# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datapipe', 'datapipe.store']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0.0,<10.0.0',
 'PyYAML>=5.3.1',
 'SQLAlchemy>=1.4.25,<2.0.0',
 'cityhash>=0.4.2,<0.5.0',
 'cloudpickle>=1.6.0',
 'fsspec>=2021.11.1',
 'iteration-utilities>=0.11.0',
 'numpy>=1.21.0,<2.0.0',
 'opentelemetry-api>=1.8.0,<2.0.0',
 'opentelemetry-instrumentation-sqlalchemy==0.35b0',
 'opentelemetry-sdk>=1.8.0,<2.0.0',
 'pandas>=1.2.0,<2.0.0',
 'psycopg2_binary>=2.8.4',
 'tqdm>=4.60.0',
 'traceback-with-variables>=2.0.4,<3.0.0']

extras_require = \
{'excel': ['xlrd>=2.0.1', 'openpyxl>=3.0.7'],
 'gcsfs': ['gcsfs>=2021.11.1'],
 'milvus': ['pymilvus>=2.0.2,<3.0.0'],
 'redis': ['redis>=4.3.4,<5.0.0'],
 's3fs': ['s3fs>=2021.11.1'],
 'sqlite': ['pysqlite3-binary>=0.5.0,<0.6.0',
            'sqlalchemy-pysqlite3-binary>=0.0.4,<0.0.5']}

setup_kwargs = {
    'name': 'datapipe-core',
    'version': '0.11.12.dev1',
    'description': '',
    'long_description': 'None',
    'author': 'Andrey Tatarinov',
    'author_email': 'a@tatarinov.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
