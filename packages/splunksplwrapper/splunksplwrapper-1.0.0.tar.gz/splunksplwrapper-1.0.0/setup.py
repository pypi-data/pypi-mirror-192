# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splunksplwrapper',
 'splunksplwrapper.app',
 'splunksplwrapper.connector',
 'splunksplwrapper.exceptions',
 'splunksplwrapper.log',
 'splunksplwrapper.manager',
 'splunksplwrapper.manager.confs',
 'splunksplwrapper.manager.confs.rest',
 'splunksplwrapper.manager.confs.sdk',
 'splunksplwrapper.manager.indexes',
 'splunksplwrapper.manager.indexes.rest',
 'splunksplwrapper.manager.indexes.sdk',
 'splunksplwrapper.manager.jobs',
 'splunksplwrapper.manager.jobs.rest',
 'splunksplwrapper.manager.jobs.sdk',
 'splunksplwrapper.manager.roles',
 'splunksplwrapper.manager.roles.sdk',
 'splunksplwrapper.manager.saved_searches',
 'splunksplwrapper.manager.saved_searches.sdk',
 'splunksplwrapper.manager.users',
 'splunksplwrapper.manager.users.sdk',
 'splunksplwrapper.misc',
 'splunksplwrapper.splunk',
 'splunksplwrapper.util']

package_data = \
{'': ['*']}

install_requires = \
['defusedxml>=0.7.1,<0.8.0',
 'future>=0.18.2,<0.19.0',
 'httplib2>=0.21.0,<0.22.0',
 'splunk-sdk>=1.6.18,<2.0.0']

setup_kwargs = {
    'name': 'splunksplwrapper',
    'version': '1.0.0',
    'description': 'Package to interact with Splunk',
    'long_description': 'None',
    'author': 'Splunk',
    'author_email': 'addonfactory@splunk.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
