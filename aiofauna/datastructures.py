from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Generic, Iterable, List, TypeVar, cast

from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module

T = TypeVar("T")


class LazyProxy(Generic[T], ABC):
    """
    A LazyLoading proxy object that defers the loading of an object until it is accessed.
    It generates types dynamically, so it can be used as a base class for other classes.
    These classes will benefit from the lazy loading behavior which improves performance.
    Also, it can be used as a decorator for functions, which will be called when the function is called.
    Subclasses must implement the __load__ method to provide the logic for loading the proxied object.
    Usage:
    1. Subclass LazyProxy and implement the __load__ method.
    2. Accessing attributes, calling methods, or using other operations on the LazyProxy instance will trigger
         the loading of the proxied object.
    """

    def __init__(self) -> None:
        self.__proxied: T | None = None

    def __getattr__(self, attr: str) -> object:
        return getattr(self.__get_proxied__(), attr)

    def __repr__(self) -> str:
        return repr(self.__get_proxied__())

    def __dir__(self) -> Iterable[str]:
        return self.__get_proxied__().__dir__()

    def __get_proxied__(self) -> T:
        proxied = self.__proxied
        if proxied is not None:
            return proxied

        self.__proxied = proxied = self.__load__()
        return proxied

    def __set_proxied__(self, value: T) -> None:
        self.__proxied = value

    def __as_proxied__(self) -> T:
        """Helper method that returns the current proxy, typed as the loaded object"""
        return cast(T, self)

    @abstractmethod
    def __load__(self) -> T:
        ...


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


class UploadFile(BaseModel):
    """
    File Upload Model
    """

    filename: str
    content_type: str
    data: bytes
    size: int
    headers: Dict[str, str]
