# -*- coding=utf-8 -*-

"""Utilitary module for debugging."""


from pathlib import Path
from typing import Iterator

from revsymg.index_lib import IndexT

from khloraascaf.multiplied_doubled_contigs_graph import OccOrCT
from khloraascaf.result import ScaffoldingResult


# DOC: module debug
# ============================================================================ #
#                                   CONSTANTS                                  #
# ============================================================================ #
# ---------------------------------------------------------------------------- #
#                                     Files                                    #
# ---------------------------------------------------------------------------- #
#
# Vertices of the regions
#
VERTICES_OF_REGIONS_PREFIX = 'vertices_of_regions'
VERTICES_OF_REGIONS_EXT = 'tsv'


# ============================================================================ #
#                                   FUNCTIONS                                  #
# ============================================================================ #
# ---------------------------------------------------------------------------- #
#                                     Write                                    #
# ---------------------------------------------------------------------------- #
def write_vertices_of_regions(result: ScaffoldingResult,
                              vertices_of_regions_path: Path):
    """Write the regions' vertex file.

    # DOC: describe the output file here

    Parameters
    ----------
    result : ScaffoldingResult
        Previous scaffolding result
    vertices_of_regions_path : Path
        Path of the future file containing the regions' vertices
    """
    with open(vertices_of_regions_path, 'w', encoding='utf-8') as f_out:
        for region_index in range(result.number_regions()):

            line: str = f'{region_index}'
            for occorc in result.region_occorc(region_index):
                line += f'\t{occorc}'
            f_out.write(line + '\n')


# ---------------------------------------------------------------------------- #
#                                     Read                                     #
# ---------------------------------------------------------------------------- #
def read_vertices_of_regions(vertices_of_regions_path: Path) -> (
        Iterator[tuple[IndexT, list[OccOrCT]]]):
    """Read the regions' vertices file.

    Parameters
    ----------
    vertices_of_regions_path : Path
        Path of the future file containing the regions' vertices

    Yields
    ------
    IndexT
        Index of the region
    list of OccOrCT
        List of vertices of the region
    """
    # TOTEST: read_vertices_of_regions
    with open(vertices_of_regions_path, 'r', encoding='utf-8') as cor_in:
        for region_ind, line in enumerate(cor_in):
            l_occorcstr = line.split('\t')[1:]
            vertices_of_region: list[OccOrCT] = [
                eval(occorcstr)
                for occorcstr in l_occorcstr
            ]
            yield region_ind, vertices_of_region


# ---------------------------------------------------------------------------- #
#                                Format Filename                               #
# ---------------------------------------------------------------------------- #
def fmt_vertices_of_regions_filename(instance_name: str) -> str:
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
    return (f'{VERTICES_OF_REGIONS_PREFIX}_{instance_name}'
            f'.{VERTICES_OF_REGIONS_EXT}')
