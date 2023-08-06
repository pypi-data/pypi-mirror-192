# -*- coding=utf-8 -*-

"""Caffolding result's module: structures and utils."""


from __future__ import annotations

import sys
from queue import LifoQueue, Queue
from typing import Iterator, Optional

from revsymg.index_lib import FORWARD_INT, REVERSE_INT, IndexT, OrT

from khloraascaf.exceptions import NotACircuit
from khloraascaf.ilp.dirf_sets import dirf_canonical, dirf_other
from khloraascaf.ilp.invf_sets import invf_canonical, invf_other
from khloraascaf.ilp.pulp_var_db import (
    BIN_THRESHOLD,
    PuLPVarDirFModel,
    PuLPVarInvFModel,
    PuLPVarModelT,
)
from khloraascaf.multiplied_doubled_contigs_graph import (
    COCC_IND,
    COR_IND,
    MDCGraph,
    OccOrCT,
)


# ============================================================================ #
#                                     TYPES                                    #
# ============================================================================ #
# ---------------------------------------------------------------------------- #
#                                Genomic Regions                               #
# ---------------------------------------------------------------------------- #
GenRegionMapT = list[tuple[IndexT, OrT]]
GenRegionT = list[OccOrCT]


# ============================================================================ #
#                                     CLASS                                    #
# ============================================================================ #
class ScaffoldingResult():
    """Scaffolding result class.

    An instance contains a genomic regions map and each genomic regions'
    oriented contigs.

    Warning
    -------
    The result corresponds to the linear path in mdcg so the circularity is not
    fixed here, i.e. the first region begins by mdcg.occorc_start() and the last
    region finishes by mdcg.occorc_terminal()
    """

    # DOC: add to docstring example to get regions' orc from result

    __NO_OPT_VALUE = 0

    def __init__(self, instance_name: str):
        """The Initializer."""
        self.__instance_name = instance_name
        #
        # Genomic region
        #
        self.__regions_map: GenRegionMapT = []
        self.__regions_occorc: list[GenRegionT] = []
        self.__unique_regions: list[IndexT] = []
        self.__ir_regions: list[IndexT] = []
        self.__dr_regions: list[IndexT] = []
        #
        # ILP optimal value
        #
        self.__opt_value: int = self.__NO_OPT_VALUE

    # ~*~ Setter ~*~

    def set_opt_value(self, opt_value: int):
        """Set ILP optimal value.

        Parameters
        ----------
        opt_value : int
            The optimal value to set
        """
        self.__opt_value = opt_value

    def clear_regions(self):
        """Delete the current regions result."""
        self.__regions_map.clear()
        self.__regions_occorc.clear()
        self.__unique_regions.clear()
        self.__ir_regions.clear()
        self.__dr_regions.clear()

    def add_region(self, region_code: int,
                   region_index: Optional[IndexT] = None) -> IndexT:
        """Add a region.

        Parameters
        ----------
        region_code : int
            Region code (0: UNIQUE; 1: IR; 2: DR)
        region_index : IndexT, optional
            Index of an already existing region, else None

        Returns
        -------
        IndexT
            Region's index
        """
        #
        # Non-existing region
        #
        if region_index is None:
            region_index = len(self.__regions_occorc)
            self.__regions_occorc.append([])
            self.__regions_map.append((region_index, FORWARD_INT))
            if region_code == 0:  # pylint: disable=compare-to-zero
                self.__unique_regions.append(region_index)
            elif region_code == 1:
                self.__ir_regions.append(region_index)
            elif region_code == 2:
                self.__dr_regions.append(region_index)
            else:
                # TODO: exception wrong region code
                sys.exit('ERROR: wrong region code')
        #
        # Already existing region (repeat)
        #
        else:
            if region_code == 0:  # pylint: disable=compare-to-zero
                # TODO: exception can't add twice a UNIQ region
                sys.exit("ERROR: can't add twice a UNIQ region")
            if region_code == 1:
                self.__regions_map.append((region_index, REVERSE_INT))
            elif region_code == 2:
                self.__regions_map.append((region_index, FORWARD_INT))
            else:
                # TODO: exception wrong region code
                sys.exit('ERROR: wrong region code')
        return region_index

    def add_occorc_to_region(self, v: OccOrCT, region_index: IndexT):
        """Add v to the region denoted by its index.

        Parameters
        ----------
        v : OccOrCT
            Multiplied oriented contig
        region_index : IndexT
            Region's index
        """
        self.__regions_occorc[region_index].append(v)

    def set_instance_name(self, instance_name: str):
        """Set instance name.

        Parameters
        ----------
        instance_name : str
            Instance name
        """
        self.__instance_name = instance_name

    # ~*~ Getter ~*~

    def instance_name(self) -> str:
        """Return the instance name.

        Returns
        -------
        str
            Instance name
        """
        return self.__instance_name

    def opt_value(self) -> int:
        """ILP optimal value.

        Returns
        -------
        int
            ILP optimal value
        """
        return self.__opt_value

    def number_regions(self) -> int:
        """Returns the number of regions.

        Returns
        -------
        int
            Number of regions
        """
        return len(self.__regions_occorc)

    def unique_regions(self) -> Iterator[IndexT]:
        """Iterate over unique regions index.

        Yields
        ------
        IndexT
            Unique region index
        """
        yield from self.__unique_regions

    def ir_regions(self) -> Iterator[IndexT]:
        """Iterate over inverted repeats index.

        Yields
        ------
        IndexT
            Inverted repeats index
        """
        yield from self.__ir_regions

    def dr_regions(self) -> Iterator[IndexT]:
        """Iterate over directed repeats index.

        Yields
        ------
        IndexT
            Directed repeats index
        """
        yield from self.__dr_regions

    def map_of_regions(self) -> Iterator[tuple[IndexT, OrT]]:
        """Iterate over the regions and their orientation.

        Yields
        ------
        IndexT
            Region's index
        OrT
            Region's orientation
        """
        yield from self.__regions_map

    def region_occorc(self, region_index: IndexT) -> Iterator[OccOrCT]:
        """Iterate over the multiplied oriented contig of the region.

        Parameters
        ----------
        region_index : IndexT
            Region's index

        Yields
        ------
        OccOrCT
            Multiplied oriented contig of the region
        """
        yield from self.__regions_occorc[region_index]


# ============================================================================ #
#                                   FUNCTIONS                                  #
# ============================================================================ #
# ---------------------------------------------------------------------------- #
#                                Fill The Result                               #
# ---------------------------------------------------------------------------- #
def path_to_regions(mdcg: MDCGraph,
                    starter_vertex: OccOrCT,
                    var: PuLPVarModelT,
                    result: ScaffoldingResult):
    """Extract regions from optimal path.

    Parameters
    ----------
    mdcg : MDCGraph
        Multiplied doubled contig graph
    starter_vertex : OccOrCT
        Starter vertex
    var : PuLPVarModelT
        PuLP variables
    result : ScaffoldingResult
        Scaffolding result with regions
    """
    # ------------------------------------------------------------------------ #
    # Manage paired fragments
    # ------------------------------------------------------------------------ #
    # TODO: think about e.g. several IR & how to adapt these functions bellow?
    #   * if the pulp model want to keep subpath with avoiding the previous
    #       repeated fragments to be paired, then is it sufficient to read
    #       previous repeated region in result object?
    set_invf_paired = __create_set_invf_paired(var, result)
    set_dirf_paired = __create_set_dirf_paired(var, result)

    # ------------------------------------------------------------------------ #
    # Init regions
    # ------------------------------------------------------------------------ #
    result.clear_regions()
    # reg_code:
    #   - 0: UNIQUE
    #   - 1: IR
    #   - 2: DR
    reg_code = 0
    region_index = result.add_region(reg_code)

    initial_vertex = __find_initial(
        mdcg, starter_vertex, var, set_invf_paired, set_dirf_paired)

    u: OccOrCT = initial_vertex  # previous v
    v: Optional[OccOrCT] = initial_vertex

    #
    # Region IR: LIFO, DR: FIFO
    #
    # XXX: no order between pairs of repeats
    #   - for the moment, the pairs of contiguous repeat are not considered
    #       ordered (e.g. pairs of contiguous IR should be lifo, DR fifo)
    ir_lifo: dict[IndexT, LifoQueue[OccOrCT]] = {}
    dr_fifo: dict[IndexT, Queue[OccOrCT]] = {}
    #
    # Canonical to the region's index: repeat was discovered
    #
    ir_canonical_reg: dict[OccOrCT, IndexT] = {}
    dr_canonical_reg: dict[OccOrCT, IndexT] = {}

    # ------------------------------------------------------------------------ #
    # Walk into the solution path
    # ------------------------------------------------------------------------ #
    while v is not None:
        new_reg_code = __get_region_code(v, set_invf_paired, set_dirf_paired)
        #
        # Type is contiguous
        #
        if new_reg_code == reg_code:
            #
            # Previous UNIQ region
            #
            if new_reg_code == 0:  # pylint: disable=compare-to-zero
                result.add_occorc_to_region(v, region_index)
            #
            # Previous or new IR region
            #
            elif new_reg_code == 1:
                canonical_invf = invf_canonical(v)
                #
                # Contiguous or new forward IR region
                #
                if canonical_invf not in ir_canonical_reg:
                    #
                    # Contiguous forward IR region
                    #
                    if __is_repeat_contiguous(u, v, var, new_reg_code):
                        result.add_occorc_to_region(v, region_index)
                        ir_lifo[region_index].put(invf_other(v))
                        ir_canonical_reg[canonical_invf] = region_index
                    #
                    # New forward IR region
                    #
                    else:
                        region_index = result.add_region(new_reg_code)
                        result.add_occorc_to_region(v, region_index)
                        ir_lifo[region_index] = LifoQueue()
                        ir_lifo[region_index].put(invf_other(v))
                        ir_canonical_reg[canonical_invf] = region_index

                #
                # IR region already existing
                #
                else:
                    #
                    # New reverse IR region
                    #
                    if region_index != ir_canonical_reg[canonical_invf]:
                        region_index = ir_canonical_reg[canonical_invf]
                        result.add_region(new_reg_code, region_index)
                    assert v == ir_lifo[region_index].get()
            #
            # Previous or new DR region
            #
            elif new_reg_code == 2:
                #
                # Contiguous or new first DR region
                #
                canonical_dirf = dirf_canonical(v)
                if canonical_dirf not in dr_canonical_reg:
                    #
                    # Contiguous first DR region
                    #
                    # FIXME: region_index provides the first repeat occorc
                    if __is_repeat_contiguous(u, v, var, new_reg_code):
                        result.add_occorc_to_region(v, region_index)
                        dr_fifo[region_index].put(dirf_other(v))
                        dr_canonical_reg[canonical_dirf] = region_index
                    #
                    # New first DR region
                    #
                    else:
                        region_index = result.add_region(new_reg_code)
                        result.add_occorc_to_region(v, region_index)
                        dr_fifo[region_index] = Queue()
                        dr_fifo[region_index].put(dirf_other(v))
                        dr_canonical_reg[canonical_dirf] = region_index

                #
                # DR region already existing
                #
                else:
                    #
                    # New second DR region
                    #
                    if region_index != dr_canonical_reg[canonical_dirf]:
                        region_index = dr_canonical_reg[canonical_dirf]
                        result.add_region(new_reg_code, region_index)
                    assert v == dr_fifo[region_index].get()
        #
        # New type of region
        #
        else:
            #
            # New UNIQ region
            #
            if new_reg_code == 0:  # pylint: disable=compare-to-zero
                region_index = result.add_region(new_reg_code)
                result.add_occorc_to_region(v, region_index)
            #
            # New or already existing IR region
            #
            elif new_reg_code == 1:
                canonical_invf = invf_canonical(v)
                #
                # New forward IR
                #
                if canonical_invf not in ir_canonical_reg:
                    region_index = result.add_region(new_reg_code)
                    result.add_occorc_to_region(v, region_index)
                    ir_lifo[region_index] = LifoQueue()
                    ir_lifo[region_index].put(invf_other(v))
                    ir_canonical_reg[canonical_invf] = region_index
                #
                # New reverse IR
                #
                else:
                    region_index = ir_canonical_reg[canonical_invf]
                    result.add_region(new_reg_code, region_index)
                    assert v == ir_lifo[region_index].get()
            #
            # New or already existing DR region
            #
            elif new_reg_code == 2:
                canonical_dirf = dirf_canonical(v)
                #
                # New first DR
                #
                if canonical_dirf not in dr_canonical_reg:
                    region_index = result.add_region(new_reg_code)
                    result.add_occorc_to_region(v, region_index)
                    dr_fifo[region_index] = Queue()
                    dr_fifo[region_index].put(dirf_other(v))
                    dr_canonical_reg[canonical_dirf] = region_index
                #
                # New second DR
                #
                else:
                    region_index = dr_canonical_reg[canonical_dirf]
                    result.add_region(new_reg_code, region_index)
                    assert v == dr_fifo[region_index].get()

        reg_code = new_reg_code
        u = v
        v = __succ_in_path(v, mdcg, var, initial_vertex)


# ---------------------------------------------------------------------------- #
#                               Walk In The Path                               #
# ---------------------------------------------------------------------------- #
def __pred_in_path(v: OccOrCT, mdcg: MDCGraph,
                   var: PuLPVarModelT, initial_vertex: OccOrCT) -> (
        Optional[OccOrCT]):
    """Return the predecessor of vertex v in solution path.

    Stop if the predecessor is the initial vertex.

    Parameters
    ----------
    v : OccOrCT
        Vertex
    mdcg : MDCGraph
        Multiplied doubled contig graph
    var : PuLPVarModelT
        PuLP variables
    initial_vertex : OccOrCT
        Starter vertex

    Returns
    -------
    OccOrCT, optional
        The previous vertex in solution path, None if it is the
        initial vertex

    Raises
    ------
    NotACircuit
        If the path is not a circuit
    """
    for u in mdcg.multiplied_preds(v):
        if var.x[u, v].varValue > BIN_THRESHOLD:
            if u == initial_vertex:
                return None
            return u
    raise NotACircuit()


def __succ_in_path(v: OccOrCT, mdcg: MDCGraph,
                   var: PuLPVarModelT, initial_vertex: OccOrCT) -> (
        Optional[OccOrCT]):
    """Return the successor of vertex v in solution path.

    Stop if the successor is the initial vertex.

    Parameters
    ----------
    v : OccOrCT
        Vertex
    mdcg : MDCGraph
        Multiplied doubled contig graph
    var : PuLPVarModelT
        PuLP variables
    initial_vertex : OccOrCT
        Starter vertex

    Returns
    -------
    OccOrCT, optional
        The next vertex in solution path, None if it is the
        initial vertex

    Raises
    ------
    NotACircuit
        If the path is not a circuit
    """
    for w in mdcg.multiplied_succs(v):
        if var.x[v, w].varValue > BIN_THRESHOLD:
            if w == initial_vertex:
                return None
            return w
    raise NotACircuit()


# ---------------------------------------------------------------------------- #
#                                Initialisation                                #
# ---------------------------------------------------------------------------- #
def __create_set_invf_paired(var: PuLPVarModelT,
                             result: ScaffoldingResult) -> set[OccOrCT]:
    """Create set of canonical of paired inverted fragments.

    Parameters
    ----------
    var : PuLPVarModelT
        PuLP variables
    result : ScaffoldingResult
        Scaffolding result

    Returns
    -------
    set of OccOrCT
        Set of canonical of paired inverted fragments
    """
    set_invf_paired: set[OccOrCT] = set()
    #
    # Add old inverted fragments pairing
    #
    for region_index in result.ir_regions():
        for v in result.region_occorc(region_index):
            set_invf_paired.add(invf_canonical(v))
    #
    # Add new inverted fragments pairing
    #
    if isinstance(var, PuLPVarInvFModel):
        for p, var_p in var.m.items():
            if var_p.value() > BIN_THRESHOLD:
                set_invf_paired.add(p[FORWARD_INT])
    return set_invf_paired


def __create_set_dirf_paired(var: PuLPVarModelT,
                             result: ScaffoldingResult) -> set[OccOrCT]:
    """Create set of canonical of paired directed fragments.

    Parameters
    ----------
    var : PuLPVarModelT
        PuLP variables
    result : ScaffoldingResult
        Scaffolding result

    Returns
    -------
    set of OccOrCT
        Set of canonical of paired directed fragments
    """
    set_dirf_paired: set[OccOrCT] = set()
    #
    # Add old directed fragments pairing
    #
    for region_index in result.dr_regions():
        for v in result.region_occorc(region_index):
            set_dirf_paired.add(dirf_canonical(v))
    #
    # Add new directed fragments pairing
    #
    if isinstance(var, PuLPVarDirFModel):
        for p, var_p in var.m.items():
            if var_p.value() > BIN_THRESHOLD:
                set_dirf_paired.add(p[FORWARD_INT])
    return set_dirf_paired


# pylint: disable=too-many-arguments
def __find_initial(mdcg: MDCGraph, starter_vertex: OccOrCT,
                   var: PuLPVarModelT,
                   set_invf_paired: set[OccOrCT],
                   set_dirf_paired: set[OccOrCT]) -> OccOrCT:
    """The first vertex of the starter's region.

    In case of circular unique region, it returns starter_vertex.

    Parameters
    ----------
    mdcg : MDCGraph
        Multiplied doubled contig graph
    starter_vertex : OccOrCT
        Starter vertex
    var : PuLPVarModelT
        PuLP variables
    set_invf_paired : set of OccOrCT
        Set of canonical of paired inverted fragments
    set_dirf_paired : set of OccOrCT
        Set of canonical of paired directed fragments

    Returns
    -------
    OccOrCT
        The first vertex of the starter's region
    """
    v: OccOrCT = starter_vertex
    u: Optional[OccOrCT] = __pred_in_path(
        starter_vertex, mdcg, var, starter_vertex)
    # pylint: disable=compare-to-zero
    while (u is not None
           and __get_region_code(u, set_invf_paired, set_dirf_paired) == 0
           ):
        v = u
        u = __pred_in_path(v, mdcg, var, starter_vertex)
    if u is None:
        return starter_vertex
    return v


# ---------------------------------------------------------------------------- #
#                               Region Management                              #
# ---------------------------------------------------------------------------- #
def __get_region_code(v: OccOrCT, set_invf_paired: set[OccOrCT],
                      set_dirf_paired: set[OccOrCT]) -> int:
    """Get the code of the region for the multiplied oriented contig.

    Parameters
    ----------
    v : OccOrCT
        Multiplied oriented contig
    set_invf_paired : set of OccOrCT
        Set of canonical of paired inverted fragments
    set_dirf_paired : set of OccOrCT
        Set of canonical of paired directed fragments

    Returns
    -------
    int
        Code of the region (0: UNIQUE; 1: IR; 2: DR)
    """
    if dirf_canonical(v) in set_dirf_paired:
        return 2
    if ((v[COCC_IND] - v[COR_IND]) % 2 == 0  # pylint: disable=compare-to-zero
            and invf_canonical(v) in set_invf_paired):
        return 1
    return 0


def __is_repeat_contiguous(u: OccOrCT, v: OccOrCT,
                           var: PuLPVarModelT,
                           region_code: int) -> bool:
    """Answer if the repeat given by its code is contiguous.

    Parameters
    ----------
    u : OccOrCT
        Multiplied oriented contig
    v : OccOrCT
        Multiplied oriented contig
    var : PuLPVarModelT
        PuLP variables
    region_code : int
        Region's code

    Returns
    -------
    bool
        True if repeat is contiguous, else False
    """
    #
    # IR:
    #   i (= u) -> k(= v): ok, so is there l -> j?
    #
    if region_code == 1:
        return var.x[invf_other(v), invf_other(u)].varValue > BIN_THRESHOLD
    #
    # DR:
    #   i (= u) -> k(= v): ok, so is there j -> l?
    #
    if region_code == 2:
        return var.x[dirf_other(u), dirf_other(v)].varValue > BIN_THRESHOLD
    # TODO: error out of code
    return False
