"""
Molecular preprocessing pipeline components.

This package provides a comprehensive set of preprocessing steps for molecular data processing
pipelines. These steps can be chained together to clean, standardize, and validate molecular
datasets commonly used in cheminformatics and drug discovery.

The preprocessing steps inherit from the base `PreprocessingStep` class and can be easily combined
to create custom preprocessing pipelines. Each step operates on molecular records and can transform
molecules, report problems, or filter out invalid structures.

Available Preprocessing Steps
-----------------------------

- `CheckValidSmiles` : Validates molecules through SMILES round-trip conversion
- `Sanitize` : Validates and corrects molecular structures using RDKit sanitization
- `FilterByWeight` : Filters molecules based on molecular weight thresholds
- `FilterByElement` : Filters molecules based on allowed elemental composition
- `StandardizeWithCsp` : Standardizes molecules using ChEMBL Structure Pipeline
- `GetParentMolWithCsp` : Extracts parent molecules using ChEMBL Structure Pipeline
- `RemoveHydrogens` : Removes hydrogen atoms from molecular representations
- `RemoveSmallFragments` : Removes small fragments, keeping only the largest component
- `RemoveStereochemistry` : Removes stereochemical information from molecules

Base Classes
------------

- `PreprocessingStep` : Abstract base class for all preprocessing steps

Examples
--------

Basic usage of individual preprocessing steps:

>>> from nerdd_module.preprocessing import FilterByWeight, RemoveHydrogens, Sanitize
>>>
>>> # Create preprocessing steps
>>> weight_filter = FilterByWeight(min_weight=150, max_weight=500)
>>> hydrogen_remover = RemoveHydrogens()
>>> sanitizer = Sanitize()

Creating a complete preprocessing pipeline:

>>> from nerdd_module.preprocessing import (
...     CheckValidSmiles, FilterByElement, RemoveSmallFragments,
...     Sanitize, StandardizeWithCsp, ORGANIC_SUBSET
... )
>>>
>>> # Define a comprehensive preprocessing pipeline
>>> pipeline_steps = [
...     Sanitize(),                       # Sanitize molecules
...     CheckValidSmiles(),               # Validate SMILES representation
...     RemoveSmallFragments(),           # Remove salts and solvents
...     FilterByElement(ORGANIC_SUBSET),  # Keep only organic molecules
...     StandardizeWithCsp(),             # Standardize using chembl_structure_pipeline
... ]


Notes
-----
* All preprocessing steps follow the same interface defined by `PreprocessingStep`
* Steps can be chained together to create comprehensive preprocessing pipelines
* Problems encountered during preprocessing are accumulated in the record's "problems" list
* Some steps require optional dependencies (e.g., `chembl_structure_pipeline`)
* The order of preprocessing steps can significantly impact the final results

See Also
--------
nerdd_module.steps : Base classes for pipeline steps nerdd_module.problem : Problem reporting
classes used by preprocessing steps
"""

from .check_valid_smiles import *
from .chembl_structure_pipeline import *
from .filter_by_element import *
from .filter_by_weight import *
from .preprocessing_step import *
from .remove_hydrogens import *
from .remove_small_fragments import *
from .remove_stereochemistry import *
from .sanitize import *
