# Khloraa: scaffolding stage

[![Latest release](https://gitlab.com/khloraa_scaffolding/khloraa_scaffolding/-/badges/release.svg)](https://gitlab.com/khloraa_scaffolding/khloraa_scaffolding/-/releases)
[![PyPI version](https://badge.fury.io/py/khloraascaf.svg)](https://badge.fury.io/py/khloraascaf)
[![Coverage report](https://gitlab.com/khloraa_scaffolding/khloraa_scaffolding/badges/main/coverage.svg)](https://gitlab.com/khloraa_scaffolding/khloraa_scaffolding/-/commits/main)
[![Pylint score](https://gitlab.com/khloraa_scaffolding/khloraa_scaffolding/-/jobs/artifacts/main/raw/pylint/pylint.svg?job=pylint)](https://gitlab.com/khloraa_scaffolding/khloraa_scaffolding/-/commits/main)
[![Mypy](https://gitlab.com/khloraa_scaffolding/khloraa_scaffolding/-/jobs/artifacts/main/raw/mypy/mypy.svg?job=mypy)](https://gitlab.com/khloraa_scaffolding/khloraa_scaffolding/-/commits/main)
[![Pipeline status](https://gitlab.com/khloraa_scaffolding/khloraa_scaffolding/badges/main/pipeline.svg)](https://gitlab.com/khloraa_scaffolding/khloraa_scaffolding/-/commits/main)
[![Documentation Status](https://readthedocs.org/projects/khloraa_scaffolding/badge/?version=latest)](https://khloraa_scaffolding.readthedocs.io/en/latest/?badge=latest)


## Quick installation

To install the `khloraascaf` package from the [PyPI repository](https://pypi.org/project/khloraascaf/), run the `pip` command :
```sh
pip install khloraascaf
```

You can find more installation details in the [docs/src/install.md](docs/src/install.md) file.


## Quick usage example

```python
from pathlib import Path

from khloraascaf import (
    DR_CODE_SUFFIX,
    IR_CODE_SUFFIX,
    UNIQUE_CODE_SUFFIX,
    scaffolding,
)
from khloraascaf.ilp import fmt_cbc_log_name
from khloraascaf.inputs import INSTANCE_NAME_DEF, SOLVER_CBC
from khloraascaf.outputs import (
    fmt_contigs_of_regions_filename,
    fmt_map_of_regions_filename,
)

#
# Prepare the scaffolding result directory
#
outdir = Path('scaffolding_result')
outdir.mkdir(exist_ok=True)
#
# Compute the scaffolding using the assembly data
#
scaffolding(
    Path('tests/data/IR_alone/contigs_attrs.tsv'),
    Path('tests/data/IR_alone/contigs_links.tsv'),
    'C0',
    solver='CBC',
    outdir=outdir,
)
#
# See which files the scaffolding has produced:
#
files = set(outdir.glob('*'))
assert len(files) == 5
#
# * The list of oriented contigs for each region
#
assert outdir / fmt_contigs_of_regions_filename(INSTANCE_NAME_DEF) in files
#
# * The list of oriented regions
#
assert outdir / fmt_map_of_regions_filename(INSTANCE_NAME_DEF) in files
#
# * CBC logs for directed repeat scaffolding
#
assert outdir / fmt_cbc_log_name(
    f'{INSTANCE_NAME_DEF}_{DR_CODE_SUFFIX}',
) in files
#
# * CBC logs for inverted repeat scaffolding
#
assert outdir / fmt_cbc_log_name(
    f'{INSTANCE_NAME_DEF}_{IR_CODE_SUFFIX}',
) in files
#
# * CBC logs for inverted repeat scaffolding then unique region scaffolding
#
assert outdir / fmt_cbc_log_name(
    f'{INSTANCE_NAME_DEF}_{IR_CODE_SUFFIX}_{UNIQUE_CODE_SUFFIX}',
) in files
```

## Changelog

You can refer to the [docs/src/changelog.md](docs/src/changelog.md) file for details.


## What next?

Find a list of ideas in the [docs/src/todo.md](docs/src/todo.md) file.


## Contributing

* If you find any errors, missing documentation or test, or you want to discuss features you would like to have, please post an issue (with the corresponding predefined template) [here](https://gitlab.com/khloraa_scaffolding/khloraa_scaffolding/-/issues).
* If you want to help me code, please post an issue or contact me. You can find coding convention in the [docs/src/contributing.md](docs/src/contributing.md) file.


## References

<!-- DOC: must update reference -->

* A part of the scaffolding method is described in this preprint:
    > 📰 Victor Epain, Dominique Lavenier, and Rumen Andonov, ‘Inverted Repeats Scaffolding for a Dedicated Chloroplast Genome Assembler’, 3 June 2022, https://doi.org/10.4230/LIPIcs.

## Licence

This work is licensed under a [GNU-GPLv3 licence](LICENCE).