# -*- coding=utf-8 -*-

"""Solve integer lieanr programs module."""


from __future__ import division

from pathlib import Path

from pulp import GUROBI_CMD, PULP_CBC_CMD, LpProblem

from khloraascaf.exceptions import WrongSolverName
from khloraascaf.inputs import (
    INSTANCE_NAME_DEF,
    OUTDIR_DEF,
    SOLVER_CBC,
    SOLVER_GUROBI,
)


# ============================================================================ #
#                                   CONSTANTS                                  #
# ============================================================================ #
# ---------------------------------------------------------------------------- #
#                                      CBC                                     #
# ---------------------------------------------------------------------------- #
LOG_CBC_PREFIX = 'cbc'
LOG_CBC_EXT = 'log'

# ---------------------------------------------------------------------------- #
#                                    Gurobi                                    #
# ---------------------------------------------------------------------------- #
LOG_GUROBI_PREFIX = 'gurobi'
LOG_GUROBI_EXT = 'log'


# ============================================================================ #
#                                   FUNCTIONS                                  #
# ============================================================================ #
# ---------------------------------------------------------------------------- #
#                                 Solve Models                                 #
# ---------------------------------------------------------------------------- #
def solve_pulp_problem(prob: LpProblem,
                       solver: str = SOLVER_CBC,
                       outdir: Path = OUTDIR_DEF,
                       instance_name: str = INSTANCE_NAME_DEF):
    """Instanciate and solve the PuLP model.

    Parameters
    ----------
    prob : LpProblem
        PuLP problem
    solver : str, optional
        MILP solver to use ('CBC' or 'GUROBI'), by default SOLVER_CBC
    outdir : Path, optional
        Output directory path, by default OUTDIR_DEF
    instance_name : str, optional
        Instance's name, by default INSTANCE_NAME_DEF

    Raises
    ------
    WrongSolverName
        The solver name is not correct
    """
    # REFACTOR: remove default arguments?
    if solver == SOLVER_CBC:
        prob.solve(
            PULP_CBC_CMD(
                msg=0,
                logPath=(outdir / fmt_cbc_log_name(instance_name)),
            ),
        )
    elif solver == SOLVER_GUROBI:
        prob.solve(
            GUROBI_CMD(
                msg=0,
                logPath=(outdir / fmt_gurobi_log_name(instance_name)),
            ),
        )
    else:
        raise WrongSolverName(solver)


# ---------------------------------------------------------------------------- #
#                                Logs Formatters                               #
# ---------------------------------------------------------------------------- #
def fmt_gurobi_log_name(instance_name: str) -> str:
    """Format Gurobi log file path.

    Parameters
    ----------
    instance_name : str
        Instance name

    Returns
    -------
    str
        Formatted filename
    """
    return f'{instance_name}_{LOG_GUROBI_PREFIX}.{LOG_GUROBI_EXT}'


def fmt_cbc_log_name(instance_name: str) -> str:
    """Format CBC log file path.

    Parameters
    ----------
    instance_name : str
        Instance name

    Returns
    -------
    str
        Formatted filename
    """
    return f'{instance_name}_{LOG_CBC_PREFIX}.{LOG_CBC_EXT}'
