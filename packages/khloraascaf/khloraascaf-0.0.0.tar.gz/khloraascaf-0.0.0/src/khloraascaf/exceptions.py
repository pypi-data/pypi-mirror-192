# -*- coding=utf-8 -*-

"""Scaffolding exceptions module."""

from typing import Any


# ============================================================================ #
#                                    CLASSES                                   #
# ============================================================================ #
class WrongSolverName(Exception):
    """Wrong solver name exception."""

    def __init__(self, solver: str):
        """The Initializer."""
        super().__init__()
        self.__solver = solver

    def __str__(self) -> str:
        """Print the exception message.

        Returns
        -------
        str
            Exception message
        """
        return f'ERROR: the solver name {self.__solver} is not correct\n'


# ---------------------------------------------------------------------------- #
#                                Prioritise ILP                                #
# ---------------------------------------------------------------------------- #
class CannotPrioritiseILP(Exception):
    """ILP prioritising exception."""

    def __init__(self, l_name_opt: list[tuple[str, Any]]):
        """The Initializer."""
        super().__init__()
        self.__l_name_opt = l_name_opt

    def __str__(self) -> str:
        """Print the exception message.

        Returns
        -------
        str
            Exception message
        """
        msg = 'ERROR: impossible to prioritise the optimisation problems.\n'
        for name, value in self.__l_name_opt:
            msg += f'\t* {name} optimal value: {value}\n'
        return msg


# ---------------------------------------------------------------------------- #
#                                Unfeasible ILP                                #
# ---------------------------------------------------------------------------- #
class _UnfeasibleILP(Exception):
    """ILP problem unfeasible exception."""

    _PROBLEM_ID = 'THE PROBLEM'

    def __str__(self) -> str:
        """Print the exception message.

        Returns
        -------
        str
            Exception message
        """
        return (
            'ERROR: the following problem is unfeasible:\n'
            f'\t{self._PROBLEM_ID}\n'
        )


class UnfeasibleIR(_UnfeasibleILP):
    """IR optimisation problem unfeasible exception."""

    _PROBLEM_ID = 'Find the best inverted repeats'


class UnfeasibleDR(_UnfeasibleILP):
    """DR optimisation problem unfeasible exception."""

    _PROBLEM_ID = 'Find the best directed repeats'


class UnfeasibleUNIQUE(_UnfeasibleILP):
    """UNIQUE optimisation problem unfeasible exception."""

    _PROBLEM_ID = 'Find the best unique regions'


# ---------------------------------------------------------------------------- #
#                                 Result Error                                 #
# ---------------------------------------------------------------------------- #
class NotACircuit(Exception):
    """Not a circuit exception."""

    def __str__(self) -> str:
        """Print the exception message.

        Returns
        -------
        str
            Exception message
        """
        return 'ERROR: the found path is not a circuit'
