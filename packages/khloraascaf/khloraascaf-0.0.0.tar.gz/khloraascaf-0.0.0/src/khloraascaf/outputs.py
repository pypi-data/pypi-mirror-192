# -*- coding=utf-8 -*-

"""Output of scaffolding subcommand."""

from pathlib import Path
from typing import Iterator, Literal, Optional

from revsymg.index_lib import IndexT, IndOrT, OrT

from khloraascaf.inputs import (
    FORWARD_STR,
    REVERSE_STR,
    STR_ORIENT,
    IdCT,
    OrStrT,
)
from khloraascaf.multiplied_doubled_contigs_graph import (
    CIND_IND,
    COR_IND,
    MDCGraphIDContainer,
)
from khloraascaf.result import ScaffoldingResult


# DOC: missing docstrings for constants
# ============================================================================ #
#                                     TYPES                                    #
# ============================================================================ #
OrCT = tuple[IdCT, OrT]

# ============================================================================ #
#                                   CONSTANTS                                  #
# ============================================================================ #
#
# For OrCT type
#
ORC_ID_IND: Literal[0] = 0
ORC_OR_IND: Literal[1] = 1

# ---------------------------------------------------------------------------- #
#                                 Orientations                                 #
# ---------------------------------------------------------------------------- #
#
# Transformed orientation integer -> string
#
ORIENT_INT_STR: tuple[OrStrT, OrStrT] = (FORWARD_STR, REVERSE_STR)

# ---------------------------------------------------------------------------- #
#                                     Files                                    #
# ---------------------------------------------------------------------------- #
#
# Contigs of the Regions
#
CONTIGS_OF_REGIONS_PREFIX: Literal['contigs_of_regions'] = 'contigs_of_regions'
CONTIGS_OF_REGIONS_EXT: Literal['tsv'] = 'tsv'
#
# Map of the regions
#
MAP_OF_REGIONS_PREFIX: Literal['map_of_regions'] = 'map_of_regions'
MAP_OF_REGIONS_EXT: Literal['tsv'] = 'tsv'


# ============================================================================ #
#                                   FUNCTIONS                                  #
# ============================================================================ #
# ---------------------------------------------------------------------------- #
#                                     Write                                    #
# ---------------------------------------------------------------------------- #
def write_contigs_of_regions(
        result: ScaffoldingResult, contigs_of_regions_path: Path,
        id_container: Optional[MDCGraphIDContainer] = None):
    """Write the regions' contigs file.

    # DOC: describe the output file here

    Parameters
    ----------
    result : ScaffoldingResult
        Previous scaffolding result
    contigs_of_regions_path : Path
        Path of the future file containing the regions' oriented contigs
    id_container : MDCGraphIDContainer, optional
        Identifiers container for the graph, by default None
    """
    with open(contigs_of_regions_path, 'w', encoding='utf-8') as f_out:
        for region_index in range(result.number_regions()):

            line: str = f'{region_index}'
            for occorc in result.region_occorc(region_index):
                if id_container is not None:
                    line += '\t' + str(
                        id_container.vertex_to_contig(occorc[CIND_IND]),
                    )
                else:
                    line += f'\t{occorc[CIND_IND]}'
                line += f'\t{ORIENT_INT_STR[occorc[COR_IND]]}'
            f_out.write(line + '\n')


def write_map_of_regions(result: ScaffoldingResult,
                         map_of_regions_path: Path):
    """Write the region map file.

    # DOC: describe the output file here

    Parameters
    ----------
    result : ScaffoldingResult
        Scaffolding result
    map_of_regions_path : Path
        Path of the future file containing the regions' oriented contigs
    """
    with open(map_of_regions_path, 'w', encoding='utf-8') as f_out:
        for reg_ind, reg_or in result.map_of_regions():
            f_out.write(f'{reg_ind}\t{ORIENT_INT_STR[reg_or]}\n')


# ---------------------------------------------------------------------------- #
#                                     Read                                     #
# ---------------------------------------------------------------------------- #
def read_contigs_of_regions(contigs_of_regions_path: Path) -> (
        Iterator[tuple[IndexT, list[OrCT]]]):
    """Read the regions' contigs file.

    Parameters
    ----------
    contigs_of_regions_path : Path
        List of oriented contigs for each region

    Yields
    ------
    IndexT
        Index of the region
    list of OrCT
        List of oriented contigs of the region
    """
    with open(contigs_of_regions_path, 'r', encoding='utf-8') as cor_in:
        for region_ind, line in enumerate(cor_in):
            orc_of_region: list[OrCT] = []
            l_orc = line.split()[1:]
            k = 0
            while k < len(l_orc) - 1:
                orc_of_region.append(
                    (l_orc[k], STR_ORIENT[l_orc[k + 1]]),  # type: ignore
                )
                k += 2
            yield region_ind, orc_of_region


def read_map_of_regions(map_of_regions_path: Path) -> Iterator[IndOrT]:
    """Write the region map file.

    Parameters
    ----------
    map_of_regions_path : Path
        Map of regions

    Yields
    ------
    IndOrT
        The index and the orientation of the region
    """
    with open(map_of_regions_path, 'r', encoding='utf-8') as mof_in:
        for line in mof_in:
            reg_indstr, reg_orstr = line.split()
            yield IndexT(reg_indstr), STR_ORIENT[reg_orstr]  # type: ignore


# ---------------------------------------------------------------------------- #
#                                Format Filename                               #
# ---------------------------------------------------------------------------- #
def fmt_contigs_of_regions_filename(instance_name: str) -> str:
    """Format the contigs of regions filename.

    Parameters
    ----------
    instance_name : str
        Instance name

    Returns
    -------
    str
        Formatted filename
    """
    return (f'{CONTIGS_OF_REGIONS_PREFIX}_{instance_name}'
            f'.{CONTIGS_OF_REGIONS_EXT}')


def fmt_map_of_regions_filename(instance_name: str) -> str:
    """Format map of the regions filename.

    Parameters
    ----------
    instance_name : str
        Instance name

    Returns
    -------
    str
        Formatted filename
    """
    return f'{MAP_OF_REGIONS_PREFIX}_{instance_name}.{MAP_OF_REGIONS_EXT}'
