# -*- coding=utf-8 -*-

"""Algorithms for Symmetric Overlaps Graph."""

from __future__ import annotations

from typing import Union

from revsymg.exceptions import NoVertexIndex
from revsymg.graphs.merged_strands_graph import MergedStrandsRevSymGraph
from revsymg.graphs.revsym_graph import RevSymGraph
from revsymg.index_lib import IndOrT


# ============================================================================ #
#                                    DEGREE                                    #
# ============================================================================ #
def in_degree(graph: Union[RevSymGraph, MergedStrandsRevSymGraph],
              vertex: IndOrT) -> int:
    """Return the in-degree of `vertex`.

    Parameters
    ----------
    graph : RevSymGraph or MergedStrandsRevSymGraph
        Reverse symmetric graph
    vertex : IndOrT
        Oriented vertex

    Returns
    -------
    int
        In-degree

    Raises
    ------
    NoVertexIndex
        If vertex does not exist in graph
    """
    try:
        return sum(1 for _ in graph.edges().preds(vertex))
    except NoVertexIndex as no_vertex_index:
        raise no_vertex_index


def out_degree(graph: Union[RevSymGraph, MergedStrandsRevSymGraph],
               vertex: IndOrT) -> int:
    """Return the out-degree of `vertex`.

    Parameters
    ----------
    graph : RevSymGraph or MergedStrandsRevSymGraph
        Reverse symmetric graph
    vertex : IndOrT
        Oriented vertex

    Returns
    -------
    int
        Out-degree

    Raises
    ------
    NoVertexIndex
        If vertex does not exist in graph
    """
    try:
        return sum(1 for _ in graph.edges().succs(vertex))
    except NoVertexIndex as no_vertex_index:
        raise no_vertex_index


def degree(graph: Union[RevSymGraph, MergedStrandsRevSymGraph],
           vertex: IndOrT) -> int:
    """Return the degree of `vertex`.

    Parameters
    ----------
    graph : RevSymGraph or MergedStrandsRevSymGraph
        Reverse symmetric graph
    vertex : IndOrT
        Oriented vertex

    Returns
    -------
    int
        Degree

    Raises
    ------
    NoVertexIndex
        If vertex does not exist in graph
    """
    try:
        return in_degree(graph, vertex) + out_degree(graph, vertex)
    except NoVertexIndex as no_vertex_index:
        raise no_vertex_index
