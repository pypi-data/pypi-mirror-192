from typing import Union, Optional, Iterable, List, Hashable
from uuid import uuid4

from golem.core.dag.graph_node import GraphNode
from golem.core.utilities.data_structures import UniqueList


class LinkedGraphNode(GraphNode):
    """Class for node definition in the directed graph structure
    that directly stores its parent nodes.

    Args:
        nodes_from: parent nodes which information comes from
        content: ``dict`` for the content in the node

    Notes:
        The possible parameters are:
            - ``name`` - name (str) or object that performs actions in this node
            - ``params`` - dictionary with additional information that is used by
                    the object in the ``name`` field (e.g. hyperparameters values)
    """

    def __init__(self, content: Union[dict, str],
                 nodes_from: Optional[Iterable['LinkedGraphNode']] = None):
        # Wrap string into dict if it is necessary
        if isinstance(content, str):
            content = {'name': content}

        self.content: dict = content
        self._nodes_from = UniqueList(nodes_from or ())

        super().__init__()

    @property
    def nodes_from(self) -> List['LinkedGraphNode']:
        return self._nodes_from

    @nodes_from.setter
    def nodes_from(self, nodes: Optional[Iterable['LinkedGraphNode']]):
        self._nodes_from = UniqueList(nodes)

    @property
    def name(self) -> str:
        return str(self.content.get('name'))

    @property
    def parameters(self) -> dict:
        return self.content.get('params', {})

    @parameters.setter
    def parameters(self, new_parameters):
        if self.content.get('params'):
            self.content['params'].update(new_parameters)
        else:
            self.content['params'] = new_parameters

    def __hash__(self) -> int:
        return hash(self.uid)

    def __str__(self) -> str:
        return str(self.content.get('name', self.uid))

    def __repr__(self) -> str:
        return self.__str__()

    def description(self) -> str:
        node_operation = self.content.get('name')
        if node_operation is None:
            raise ValueError('Unknown content in the node: expected content[`name`], got None')
        # TODO: possibly unify with __repr__ & don't duplicate Operation.description
        if not self.parameters:
            node_label = f'n_{node_operation}'
        elif isinstance(node_operation, str):
            # If there is a string: name of operation (as in json repository)
            node_label = f'n_{node_operation}_{self.parameters}'
        else:
            # If instance of Operation is placed in 'name'
            node_label = node_operation.description(self.parameters)
        return node_label
