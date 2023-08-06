# Flow Immersive Python Client

An easy way to push data from pandas to Flow.

## Usage

Push data to Flow, identifying the dataset with a title. 
Pushing a new dataset with the same title will create a new dataset version.

```python
import pandas as pd

# Example pandas dataframe
df = pd.DataFrame({
    'name': ['John', 'Jane', 'Joe'],
    'age': [30, 25, 40],
    'city': ['New York', 'San Francisco', 'Los Angeles']
})

from flowgl import Client

# Import the client and create an instance with your credentials
client = Client(
    username=...,
    password=...,
)

# Push the dataframe to Flow by title
client.push_data(
    df,
    dataset_title='My Dataset',
)
```

If you're working with a dictionary of nodes and edges, you can use the 
`push_nodes_and_edges_dict` method, referencing the nodes list and edges list
in the provided dictionary by jsonpath.

```python
my_dict = {
    'nested_object': {
        'nodes': [
            {'id': 1, 'name': 'John'},
            {'id': 2, 'name': 'Jane'},
            {'id': 3, 'name': 'Joe'},
        ],
        'edges': [
            {'source': 1, 'target': 2},
            {'source': 2, 'target': 3},
        ]
    }
}

client.push_nodes_and_edges_dict(
    my_dict,
    nodes_jsonpath='$.nested_object.nodes',
    edges_jsonpath='$.nested_object.edges',
    dataset_title='My Dataset',
)
```