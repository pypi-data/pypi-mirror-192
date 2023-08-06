from typing import Any, Dict, Optional

import pandas as pd
from requests_toolbelt import sessions
import jsonpath_ng


class Client:
    def __init__(
        self,
        username: str,
        password: str,
        base_url: str = "https://api.flow.gl/v1/",
    ):
        self._client = sessions.BaseUrlSession(base_url=base_url)
        # get token
        response = self._client.post('access_token', json={
            'email': username,
            'grant_type': 'password',
            'password': password,
        })
        if response.status_code != 200:
            raise Exception('Failed to get access token')
        token = response.json()['data']['access_token']
        self._client.headers.update({
            'Authorization': f'Bearer {token}',
        })

    def push_data(
        self,
        data: pd.DataFrame,
        *,
        dataset_id: Optional[int] = None,
        dataset_title: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Push data (in a pandas DataFrame) to the Flow API.

        Either `dataset_id` or `dataset_title` must be specified.

        Returns the dataset object, including the dataset ID and dataset version ID.
        """
        request_kwargs = {}
        if dataset_id is None:
            if dataset_title is None:
                raise Exception('Either dataset_id or dataset_title must be specified, but both are None')

            request_kwargs['data'] = {
                'title': dataset_title,
                'source': "API",
            }
            request_kwargs['url'] = 'datasets'
            request_kwargs['method'] = 'POST'
        else:
            if dataset_title is not None:
                raise Exception('Either dataset_id or dataset_title must be specified, not both')

            request_kwargs['url'] = f'datasets/{dataset_id}'
            request_kwargs['method'] = 'PUT'
        request_kwargs['files'] = {
            'file': ('data.csv', data.to_csv(index=False)),
        }
        response = self._client.request(**request_kwargs)
        if response.status_code // 100 != 2:
            error_message = f'Code {response.status_code}'
            try:
                error_message += f', {response.json()}'
            except Exception:
                pass
            raise RuntimeError(f'Failed to push data: {error_message}')
        return response.json()['data']

    def push_nodes_and_edges_dict(
        self,
        data: Dict[str, Any],
        node_id_key: str = 'id',
        edge_source_key: str = 'source',
        edge_target_key: str = 'target',
        nodes_jsonpath: str = '$.nodes',
        edges_jsonpath: str = '$.edges',
        *,
        dataset_id: Optional[int] = None,
        dataset_title: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Push nodes and edges (in a dict) to the Flow API.

        Either `dataset_id` or `dataset_title` must be specified.

        Returns the dataset object, including the dataset ID and dataset version ID.

        The dict at `nodes_jsonpath` (default: `$.nodes`) must be a list of dicts,
        each of which must have a `node_id_key` (default `id`) with a unique value.

        The dict at `edges_jsonpath` (default: `$.edges`) must be a list of dicts,
        each of which must have `edge_source_key` (default `source`) and `edge_target_key`
        (default `target`) with values that match the `node_id_key` of a node in the nodes list.
        """
        # parse jsonpaths

        # parse nodes jsonpath
        nodes = jsonpath_ng.parse(nodes_jsonpath).find(data)
        if len(nodes) != 1:
            raise ValueError(f'Expected exactly one node list at {nodes_jsonpath}, found {len(nodes)}')
        # parse edges jsonpath
        edges = jsonpath_ng.parse(edges_jsonpath).find(data)
        if len(edges) != 1:
            raise ValueError(f'Expected exactly one edge list at {edges_jsonpath}, found {len(edges)}')

        # check that all referenced nodes exist

        # get nodes and edges
        nodes_df = pd.json_normalize(nodes[0].value)
        edges_df = pd.DataFrame(edges[0].value)
        # get node IDs
        node_ids = set(nodes_df[node_id_key].unique())
        # get edge sources and targets
        edge_sources = edges_df[edge_source_key].unique()
        edge_targets = edges_df[edge_target_key].unique()
        referenced_node_ids = set(edge_sources).union(set(edge_targets))
        # check that all referenced nodes are in the nodes list
        if not referenced_node_ids.issubset(node_ids):
            raise ValueError(f"Some nodes referenced by edges don't exist: {referenced_node_ids - node_ids}")

        # compile nodes and edges

        output_column = 'list of edges'
        # group edges by source and collect targets into a set (to remove duplicates)
        edges_series = edges_df.groupby(edge_source_key)[edge_target_key].apply(set)
        # convert to pipe-separated string
        edges_pipe_series = edges_series.map(lambda edges_list: '|'.join(str(e) for e in edges_list))
        # join edges to nodes
        nodes_df[output_column] = nodes_df[node_id_key].map(edges_pipe_series)
        # fill NaN (which are nodes without edges) with empty string
        nodes_df[output_column].fillna('', inplace=True)

        # push the nodes and edges
        return self.push_data(
            nodes_df,
            dataset_id=dataset_id,
            dataset_title=dataset_title,
        )
