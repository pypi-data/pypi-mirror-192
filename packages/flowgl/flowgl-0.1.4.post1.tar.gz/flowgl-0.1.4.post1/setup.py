# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flowgl']

package_data = \
{'': ['*']}

install_requires = \
['jsonpath-ng>=1.5.3,<2.0.0', 'requests-toolbelt>=0.10.1,<0.11.0']

setup_kwargs = {
    'name': 'flowgl',
    'version': '0.1.4.post1',
    'description': 'Flow Immersive python client for datasets API',
    'long_description': "# Flow Immersive Python Client\n\nAn easy way to push data from pandas to Flow.\n\n## Usage\n\nPush data to Flow, identifying the dataset with a title. \nPushing a new dataset with the same title will create a new dataset version.\n\n```python\nimport pandas as pd\n\n# Example pandas dataframe\ndf = pd.DataFrame({\n    'name': ['John', 'Jane', 'Joe'],\n    'age': [30, 25, 40],\n    'city': ['New York', 'San Francisco', 'Los Angeles']\n})\n\nfrom flowgl import Client\n\n# Import the client and create an instance with your credentials\nclient = Client(\n    username=...,\n    password=...,\n)\n\n# Push the dataframe to Flow by title\nclient.push_data(\n    df,\n    dataset_title='My Dataset',\n)\n```\n\nIf you're working with a dictionary of nodes and edges, you can use the \n`push_nodes_and_edges_dict` method, referencing the nodes list and edges list\nin the provided dictionary by jsonpath.\n\n```python\nmy_dict = {\n    'nested_object': {\n        'nodes': [\n            {'id': 1, 'name': 'John'},\n            {'id': 2, 'name': 'Jane'},\n            {'id': 3, 'name': 'Joe'},\n        ],\n        'edges': [\n            {'source': 1, 'target': 2},\n            {'source': 2, 'target': 3},\n        ]\n    }\n}\n\nclient.push_nodes_and_edges_dict(\n    my_dict,\n    nodes_jsonpath='$.nested_object.nodes',\n    edges_jsonpath='$.nested_object.edges',\n    dataset_title='My Dataset',\n)\n```",
    'author': 'Flow Immersive',
    'author_email': 'info@flow.gl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
