# -*- coding=utf-8 -*-

"""Scaffolding module."""

from copy import deepcopy
from pathlib import Path
from typing import Optional

from pulp import LpProblem, LpStatusOptimal

from khloraascaf.exceptions import (
    CannotPrioritiseILP,
    UnfeasibleDR,
    UnfeasibleIR,
    UnfeasibleUNIQUE,
)
from khloraascaf.ilp import solve_pulp_problem
from khloraascaf.ilp.pulp_max_dirf import intersected_dirf_model
from khloraascaf.ilp.pulp_max_invf import nested_invf_model
from khloraascaf.ilp.pulp_max_presscore import best_presscore_model
from khloraascaf.ilp.pulp_var_db import PuLPVarModelT
from khloraascaf.inputs import (
    INSTANCE_NAME_DEF,
    MULT_UPB_DEF,
    OUTDEBUG_DEF,
    OUTDIR_DEF,
    PRESSCORE_UPB_DEF,
    SOLVER_CBC,
    IdCT,
    MultT,
    PresScoreT,
)
from khloraascaf.multiplied_doubled_contigs_graph import (
    MDCGraph,
    OccOrCT,
    first_forward_occurence,
    mdcg_with_id_from_input_files,
)
from khloraascaf.outputs import (
    fmt_contigs_of_regions_filename,
    fmt_map_of_regions_filename,
    write_contigs_of_regions,
    write_map_of_regions,
)
from khloraascaf.result import ScaffoldingResult, path_to_regions
from khloraascaf.utils_debug import (
    fmt_vertices_of_regions_filename,
    write_vertices_of_regions,
)


# ============================================================================ #
#                                   CONSTANTS                                  #
# ============================================================================ #
#
# Solutions codes
#
IR_CODE_SUFFIX = 'ir'
DR_CODE_SUFFIX = 'dr'
UNIQUE_CODE_SUFFIX = 'un'


# ============================================================================ #
#                                   FUNCTIONS                                  #
# ============================================================================ #
# ---------------------------------------------------------------------------- #
#                                From Input File                               #
# ---------------------------------------------------------------------------- #
# pylint: disable=too-many-arguments
def scaffolding(
        contigs_attrs: Path,
        contigs_links: Path,
        contig_starter: IdCT,
        multiplicity_upperbound: MultT = MULT_UPB_DEF,
        presence_score_upperbound: PresScoreT = PRESSCORE_UPB_DEF,
        solver: str = SOLVER_CBC,
        outdir: Path = OUTDIR_DEF,
        instance_name: str = INSTANCE_NAME_DEF,
        debug: bool = OUTDEBUG_DEF):
    """Computes the scaffolding.

    Parameters
    ----------
    contigs_attrs : Path
        Contigs' attributes file path
    contigs_links : Path
        Contigs' links file path
    contig_starter : IdCT
        Starter contig's identifier
    multiplicity_upperbound : MultT, optional
        Multiplicities upper bound, by default MULT_UPB_DEF
    presence_score_upperbound : PresScoreT, optional
        Multiplicities upper bound, by default MULT_UPB_DEF
    solver : str, optional
        MILP solver to use (CBC or GUROBI), by default SOLVER_CBC
    outdir : Path, optional
        Output directory path, by default OUTDIR_DEF
    instance_name : str, optional
        Instance name, by default INSTANCE_NAME_DEF
    debug : bool, optional
        Output debug or not, by default False
    """
    # DOC: verify docstring
    mdcg, id_container = mdcg_with_id_from_input_files(
        contigs_attrs, contigs_links,
        multiplicity_upperbound=multiplicity_upperbound,
        presence_score_upperbound=presence_score_upperbound,
    )
    starter_vertex = first_forward_occurence(
        id_container.contig_to_vertex(contig_starter))

    # ------------------------------------------------------------------------ #
    # Find the solutions
    # ------------------------------------------------------------------------ #
    # TODO: what to do if several optimal solutions?
    #   * solution should be a list of results?
    #   * how to tell which results was selected?
    #   * metadata on the outputs (human reading)?
    solution = combine_scaffolding_problems(
        mdcg,
        starter_vertex,
        solver=solver,
        outdir=outdir,
        instance_name=instance_name,
        debug=debug,
    )

    # ------------------------------------------------------------------------ #
    # Write the solution in files
    # ------------------------------------------------------------------------ #
    #
    # The order of oriented contigs for each region
    #
    write_contigs_of_regions(
        solution,
        id_container=id_container,
        contigs_of_regions_path=(
            outdir / fmt_contigs_of_regions_filename(instance_name)
        ),
    )
    #
    # The order of oriented regions
    #
    write_map_of_regions(
        solution,
        map_of_regions_path=(
            outdir / fmt_map_of_regions_filename(instance_name)
        ),
    )


# ---------------------------------------------------------------------------- #
#                            From Mathematical Data                            #
# ---------------------------------------------------------------------------- #
def combine_scaffolding_problems(
        mdcg: MDCGraph,
        starter_vertex: OccOrCT,
        solver: str = SOLVER_CBC,
        outdir: Path = OUTDIR_DEF,
        instance_name: str = INSTANCE_NAME_DEF,
        debug: bool = OUTDEBUG_DEF) -> ScaffoldingResult:
    """Find a priority between the optimisation problems.

    Parameters
    ----------
    mdcg : MDCGraph
        Multiplied doubled contig graph
    starter_vertex : OccOrCT
        Starter vertex
    solver : str, optional
        MILP solver to use (CBC or GUROBI), by default SOLVER_CBC
    outdir : Path, optional
        Output directory path, by default OUTDIR_DEF
    instance_name : str, optional
        Instance's name, by default INSTANCE_NAME_DEF
    debug : bool, optional
        Output debug or not, by default False

    Returns
    -------
    ScaffoldingResult
        Best ILP result

    Raises
    ------
    CannotPrioritiseILP
        Choosing the best solution is not possible
    """
    ir_solution = scaffolding_inverted_repeats(
        mdcg,
        starter_vertex,
        solver=solver,
        outdir=outdir,
        instance_name=f'{instance_name}_{IR_CODE_SUFFIX}',
        debug=debug,
    )

    dr_solution = scaffolding_directed_repeats(
        mdcg,
        starter_vertex,
        solver=solver,
        outdir=outdir,
        instance_name=f'{instance_name}_{DR_CODE_SUFFIX}',
        debug=debug,
    )

    # ------------------------------------------------------------------------ #
    # First level of scaffolding
    # ------------------------------------------------------------------------ #
    if ir_solution.opt_value() > dr_solution.opt_value():
        return scaffolding_unique(
            mdcg,
            starter_vertex,
            result=ir_solution,
            solver=solver,
            outdir=outdir,
            instance_name=(
                f'{instance_name}'
                f'_{IR_CODE_SUFFIX}_{UNIQUE_CODE_SUFFIX}'
            ),
            debug=debug,
        )

    if ir_solution.opt_value() < dr_solution.opt_value():
        return scaffolding_unique(
            mdcg,
            starter_vertex,
            result=dr_solution,
            solver=solver,
            outdir=outdir,
            instance_name=(
                f'{instance_name}'
                f'_{DR_CODE_SUFFIX}_{UNIQUE_CODE_SUFFIX}'
            ),
            debug=debug,
        )

    if ir_solution.opt_value() == 0:  # pylint: disable=compare-to-zero
        return scaffolding_unique(
            mdcg,
            starter_vertex,
            solver=solver,
            outdir=outdir,
            instance_name=(
                f'{instance_name}'
                f'_{UNIQUE_CODE_SUFFIX}'
            ),
            debug=debug,
        )

    # TODO: should repeat to construct solution until no changes?
    #   * ir
    #       * ir - ir
    #           * ir - ir - ir
    #           * ir - ir - dr
    #               * ir - ir - unique
    #       * ir - dr
    #   * dr
    #       * dr - ir
    #       * dr - dr
    #
    # ------------------------------------------------------------------------ #
    # Second level of scaffolding
    # ------------------------------------------------------------------------ #
    ir_unique_solution = scaffolding_unique(
        mdcg,
        starter_vertex,
        result=ir_solution,
        solver=solver,
        outdir=outdir,
        instance_name=(
            f'{instance_name}'
            f'_{IR_CODE_SUFFIX}_{UNIQUE_CODE_SUFFIX}'
        ),
        debug=debug,
    )

    dr_unique_solution = scaffolding_unique(
        mdcg,
        starter_vertex,
        result=dr_solution,
        solver=solver,
        outdir=outdir,
        instance_name=(
            f'{instance_name}'
            f'_{DR_CODE_SUFFIX}_{UNIQUE_CODE_SUFFIX}'
        ),
        debug=debug,
    )

    if ir_unique_solution.opt_value() > dr_unique_solution.opt_value():
        return ir_unique_solution
    if ir_unique_solution.opt_value() < dr_unique_solution.opt_value():
        return dr_unique_solution

    # TODO: third level of scaffolding (ir-dr-unique) & (dr-ir-unique)

    # FIXME: show different auto with instance_name, or manually?
    #   * fill a list of tuple (name, value)
    raise CannotPrioritiseILP(
        [
            (res.instance_name(), res.opt_value())
            for res in (ir_solution,
                        dr_solution,
                        ir_unique_solution,
                        dr_unique_solution)
        ],
    )


# ---------------------------------------------------------------------------- #
#                         Specific Regions Scaffolding                         #
# ---------------------------------------------------------------------------- #
def scaffolding_inverted_repeats(
        mdcg: MDCGraph,
        starter_vertex: OccOrCT,
        result: Optional[ScaffoldingResult] = None,
        solver: str = SOLVER_CBC,
        outdir: Path = OUTDIR_DEF,
        instance_name: str = INSTANCE_NAME_DEF,
        debug: bool = OUTDEBUG_DEF) -> ScaffoldingResult:
    """Find the best inverted repeats.

    Parameters
    ----------
    mdcg : MDCGraph
        Multiplied doubled contig graph
    starter_vertex : OccOrCT
        Starter vertex
    result : ScaffoldingResult, optional
        Previous scaffolding result
    solver : str, optional
        MILP solver to use (CBC or GUROBI), by default SOLVER_CBC
    outdir : Path, optional
        Output directory path, by default OUTDIR_DEF
    instance_name : str, optional
        Instance's name, by default INSTANCE_NAME_DEF
    debug : bool, optional
        Output debug or not, by default False

    Returns
    -------
    ScaffoldingResult
        Scaffolding result

    Raises
    ------
    UnfeasibleIR
        The combinatorial problem is unfeasible
    """
    prob, var = nested_invf_model(mdcg, starter_vertex, result=result)
    solve_pulp_problem(
        prob,
        solver=solver,
        outdir=outdir,
        instance_name=instance_name,
    )
    if prob.status != LpStatusOptimal:
        raise UnfeasibleIR()

    return __fill_the_result(
        prob, var, mdcg, starter_vertex,
        outdir, instance_name, debug,
        result=result,
    )


def scaffolding_directed_repeats(
        mdcg: MDCGraph,
        starter_vertex: OccOrCT,
        result: Optional[ScaffoldingResult] = None,
        solver: str = SOLVER_CBC,
        outdir: Path = OUTDIR_DEF,
        instance_name: str = INSTANCE_NAME_DEF,
        debug: bool = OUTDEBUG_DEF) -> ScaffoldingResult:
    """Find the best directed repeats.

    Parameters
    ----------
    mdcg : MDCGraph
        Multiplied doubled contig graph
    starter_vertex : OccOrCT
        Starter vertex
    result : ScaffoldingResult, optional
        Previous scaffolding result
    solver : str, optional
        MILP solver to use (CBC or GUROBI), by default SOLVER_CBC
    outdir : Path, optional
        Output directory path, by default OUTDIR_DEF
    instance_name : str, optional
        Instance's name, by default INSTANCE_NAME_DEF
    debug : bool, optional
        Output debug or not, by default False

    Returns
    -------
    ScaffoldingResult
        Scaffolding result

    Raises
    ------
    UnfeasibleDR
        The combinatorial problem is unfeasible
    """
    prob, var = intersected_dirf_model(
        mdcg, starter_vertex,
        result=result,
    )
    solve_pulp_problem(
        prob,
        solver=solver,
        outdir=outdir,
        instance_name=instance_name,
    )
    if prob.status != LpStatusOptimal:
        raise UnfeasibleDR()

    return __fill_the_result(
        prob, var, mdcg, starter_vertex,
        outdir, instance_name, debug,
        result=result,
    )


def scaffolding_unique(
        mdcg: MDCGraph,
        starter_vertex: OccOrCT,
        result: Optional[ScaffoldingResult] = None,
        solver: str = SOLVER_CBC,
        outdir: Path = OUTDIR_DEF,
        instance_name: str = INSTANCE_NAME_DEF,
        debug: bool = OUTDEBUG_DEF) -> ScaffoldingResult:
    """Find the best unique region.

    Parameters
    ----------
    mdcg : MDCGraph
        Multiplied doubled contig graph
    starter_vertex : OccOrCT
        Starter vertex
    result : ScaffoldingResult
        Previous scaffolding result
    solver : str, optional
        MILP solver to use (CBC or GUROBI), by default SOLVER_CBC
    outdir : Path, optional
        Output directory path, by default OUTDIR_DEF
    instance_name : str, optional
        Instance's name, by default INSTANCE_NAME_DEF
    debug : bool, optional
        Output debug or not, by default False

    Returns
    -------
    ScaffoldingResult
        Scaffolding result

    Raises
    ------
    UnfeasibleUNIQUE
        The combinatorial problem is unfeasible
    """
    prob, var = best_presscore_model(mdcg, starter_vertex, result=result)
    solve_pulp_problem(
        prob,
        solver=solver,
        outdir=outdir,
        instance_name=instance_name,
    )
    if prob.status != LpStatusOptimal:
        raise UnfeasibleUNIQUE()

    return __fill_the_result(
        prob, var, mdcg, starter_vertex,
        outdir, instance_name, debug,
        result=result,
    )


def __fill_the_result(
        prob: LpProblem,
        var: PuLPVarModelT,
        mdcg: MDCGraph,
        starter_vertex: OccOrCT,
        outdir: Path,
        instance_name: str,
        debug: bool,
        result: Optional[ScaffoldingResult] = None) -> ScaffoldingResult:
    """Find the best unique region.

    Parameters
    ----------
    prob : LpProblem
        PuLP problem
    var : PuLPVarInvFModel or PuLPVarDirFModel
        PuLP variables
    mdcg : MDCGraph
        Multiplied doubled contig graph
    starter_vertex : OccOrCT
        Starter vertex
    outdir : Path
        Output directory path
    instance_name : str
        Instance's name
    debug : bool
        Output debug or not
    result : ScaffoldingResult, optional
        Previous scaffolding result, by default None

    Returns
    -------
    ScaffoldingResult
        Scaffolding result

    Raises
    ------
    UnfeasibleUNIQUE
        The combinatorial problem is unfeasible
    """
    if result is None:
        new_result = ScaffoldingResult(instance_name)
    else:
        new_result = deepcopy(result)
        new_result.set_instance_name(instance_name)
    if prob.objective.value() is not None:
        # see PuLP issue 331
        new_result.set_opt_value(prob.objective.value())

    # TODO: think about filling result with already existing result
    path_to_regions(mdcg, starter_vertex, var, new_result)

    # ------------------------------------------------------------------------ #
    # Debug
    # ------------------------------------------------------------------------ #
    if debug:
        #
        # The order of vertices for each region
        #
        write_vertices_of_regions(
            new_result,
            vertices_of_regions_path=(
                outdir
                / fmt_vertices_of_regions_filename(instance_name)
            ),
        )
        write_map_of_regions(
            new_result,
            map_of_regions_path=(
                outdir
                / fmt_map_of_regions_filename(instance_name)
            ),
        )
    return new_result
