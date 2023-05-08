from __future__ import annotations
from typing import List
from pydantic import Field, BaseModel  # pylint: disable=no-name-in-module


class Graph(BaseModel):

    """
    `Graph` is a class that represents a graph data structure. It contains a list of nodes and a list of edges. It also contains methods for adding nodes and edges to the graph, as well as methods for checking if the graph is cyclic and performing a topological sort on the graph.
    """

    nodes: List[int] = Field(default_factory=list)
    edges: List[List[int]] = Field(default_factory=list)

    def add_node(self, node: int):
        """
        The add_node method adds a node to the graph.
        """
        self.nodes.append(node)

    def add_edge(self, edge: List[int]):
        """
        The add_edge method adds an edge to the graph.
        """
        self.edges.append(edge)

    @property
    def is_cyclic(self) -> bool:
        """
        The is_cyclic property checks if the graph is cyclic.
        """

        return self._is_cyclic(self.nodes, self.edges)

    @staticmethod
    def _is_cyclic(nodes: List[int], edges: List[List[int]]) -> bool:
        """
        The _is_cyclic method iterates through each node in the graph and checks if the graph is cyclic using the _is_cyclic_helper method.
        """
        visited = set()
        for node in nodes:
            if node not in visited:
                if Graph._is_cyclic_helper(node, visited, edges):
                    return True
        return False

    @staticmethod
    def _is_cyclic_helper(node: int, visited: set, edges: List[List[int]]) -> bool:
        """
        The _is_cyclic_helper method performs a depth-first search on the node and its neighbors. If a node has already been visited, then the graph is cyclic.
        """
        if node in visited:
            return True
        visited.add(node)
        for edge in edges:
            if node in edge:
                if Graph._is_cyclic_helper(edge[1], visited, edges):
                    return True
        return False

    def topological_sort(self) -> List[int]:
        """
        The topological_sort method performs a topological sort on the graph using a modified depth-first search algorithm. It initializes a set of visited nodes and a list of sorted nodes, and then iterates through each node in the graph.
        """
        return self._topological_sort(self.nodes, self.edges)

    @staticmethod
    def _topological_sort(nodes: List[int], edges: List[List[int]]) -> List[int]:
        """
        _topological_sort_helper method to perform depth-first search on the node and its neighbors. Once all nodes have been visited, the method returns the sorted nodes.
        """
        visited = set()
        sorted_nodes = []
        for node in nodes:
            if node not in visited:
                Graph._topological_sort_helper(node, visited, edges, sorted_nodes)
        return sorted_nodes

    @staticmethod
    def _topological_sort_helper(
        node: int, visited: set, edges: List[List[int]], sorted_nodes: List[int]
    ):
        """
        The _topological_sort_helper method performs depth-first search on a node and its neighbors recursively. It adds the node to the visited set and then recursively visits its neighbors. Once all neighbors have been visited, it appends the node to the sorted list.
        """
        visited.add(node)
        for edge in edges:
            if node in edge:
                Graph._topological_sort_helper(edge[1], visited, edges, sorted_nodes)
        sorted_nodes.append(node)
