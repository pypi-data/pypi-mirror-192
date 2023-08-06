# -*- coding=utf-8 -*-

"""Intersected directed fragments PuLP ILP."""


from typing import Optional

from pulp import LpMaximize, LpProblem

from khloraascaf.ilp.pulp_circuit import (
    circuit_from_the_starter_forward,
    flow_definition,
    intermediate_in_circuit,
)
from khloraascaf.ilp.pulp_repeated_fragments import (
    adjacent_fragments,
    alpha_definition,
    forbidden_pairing_definition,
    longuest_contiguous_repeat,
    occurences_priority,
    pairs_in_path,
)
from khloraascaf.ilp.pulp_var_db import PuLPVarDirFModel
from khloraascaf.multiplied_doubled_contigs_graph import MDCGraph, OccOrCT
from khloraascaf.result import ScaffoldingResult


# ============================================================================ #
#                                  PULP MODEL                                  #
# ============================================================================ #
def intersected_dirf_model(mdcg: MDCGraph, starter_vertex: OccOrCT,
                           result: Optional[ScaffoldingResult] = None) -> (
        tuple[LpProblem, PuLPVarDirFModel]):
    """Intersected directed fragments PuLP model.

    Parameters
    ----------
    mdcg : MDCGraph
        Multiplied doubled contig graph
    starter_vertex : OccOrCT
        Starter vertex
    result : ScaffoldingResult, optional
        Previous scaffolding result, None by default

    Returns
    -------
    LpProblem
        ILP problem
    PuLPVarDirFModel
        ILP variables
    """
    # ------------------------------------------------------------------------ #
    # Constants
    # ------------------------------------------------------------------------ #
    big_m = mdcg.multiplied_card()

    # ------------------------------------------------------------------------ #
    # Problem
    # ------------------------------------------------------------------------ #
    prob = LpProblem(name='inters_dirf', sense=LpMaximize)

    # ------------------------------------------------------------------------ #
    # Variables
    # ------------------------------------------------------------------------ #
    var = PuLPVarDirFModel(mdcg, starter_vertex, big_m)

    # ------------------------------------------------------------------------ #
    # Objective function
    # ------------------------------------------------------------------------ #
    longuest_contiguous_repeat(prob, var, mdcg)

    # ------------------------------------------------------------------------ #
    # Constraints
    # ------------------------------------------------------------------------ #
    #
    # Path constraints
    #
    flow_definition(prob, var, big_m, mdcg)
    circuit_from_the_starter_forward(prob, var, mdcg, starter_vertex)
    intermediate_in_circuit(prob, var, mdcg, starter_vertex)
    #
    # Repeats constraints
    #
    pairs_in_path(prob, var, mdcg)
    alpha_definition(prob, var, mdcg, big_m)
    forbidden_pairing_definition(prob, var, mdcg)
    adjacent_fragments(prob, var, mdcg)
    #
    # Fix repeats sub-paths
    #
    if result is not None:
        pass
        # TODO: fix sub-paths
        # TODO: avoid pairs for fixed sub-paths
    else:
        #
        # Speed-up the model
        #
        occurences_priority(prob, var, mdcg)

    return prob, var
