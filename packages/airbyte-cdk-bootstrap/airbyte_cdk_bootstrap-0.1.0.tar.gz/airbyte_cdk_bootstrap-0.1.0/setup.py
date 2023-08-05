# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['airbyte_cdk_bootstrap',
 'airbyte_cdk_bootstrap.auth',
 'airbyte_cdk_bootstrap.source',
 'airbyte_cdk_bootstrap.source.miltithreading_source',
 'airbyte_cdk_bootstrap.streams',
 'airbyte_cdk_bootstrap.streams.multithread_stream']

package_data = \
{'': ['*']}

install_requires = \
['airbyte-cdk>=0.28.0,<0.29.0',
 'types-pyyaml>=6.0.12.5,<7.0.0.0',
 'types-requests>=2.28.11.12,<3.0.0.0']

setup_kwargs = {
    'name': 'airbyte-cdk-bootstrap',
    'version': '0.1.0',
    'description': 'Airbyte CDK Bootstrap lib',
    'long_description': '# airbyte-cdk-bootstrap\n\n## About\n\nPackage that must help you with fast startup your airbyte source. Based on airbyte-cdk package.\n\n## Possibilities\n\nairbyte-cdk-bootstrap can help you with:\n  - Fast setup on spec dates\n  - Fast setup on spec authorization\n  - TODO: multithread sources\n  - Fast setup on CredentialsCraft authorization',
    'author': 'dipertq',
    'author_email': '94865691+dipertq@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
