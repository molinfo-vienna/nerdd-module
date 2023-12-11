# NERDD Module

This package provides the basis to implement molecular prediction modules in the
NERDD ecosystem.

## Installation

```bash
pip install -U nerdd-module
```


## Implement your own module

A new module is created by inheriting from the ```AbstractModel``` class. A 
preprocessing pipeline can be configured via calling the constructor of the superclass.
The actual prediction procedure is implemented in ```_predict_mols```:

```python
import pandas as pd
from typing import List
from rdkit.Chem import Mol
from nerdd_module import AbstractModel

class MyModel(AbstractModel):
    def __init__(self):
        super().__init__(
            preprocessing_pipeline="chembl_structure_pipeline",
        )

    def _predict_mols(self, mols: List[Mol], custom_param: int = 5) -> pd.DataFrame:
        # implement prediction logic and return a dataframe with new columns
        # containing values per input molecule
        return pd.DataFrame(dict(predictions=[custom_param]*len(mols)))
```

For custom preprocessing, specify ```preprocessing_pipeline="custom"``` when calling
the constructor of the superclass and override the method ```_preprocess_single_mol```:

```python
class MyModel(AbstractModel):
    def __init__(self):
        # important:
        super().__init__(preprocessing_pipeline="custom")

    def _preprocess_single_mol(self, mol: Mol) -> Tuple[Mol, List[str]]:
        # implement custom preprocessing logic here 
        # return preprocessed molecule and a list of error messages
        return preprocessed_mol, errors
    # ...
```


## Contribute

1. Fork and clone the code
2. Install test dependencies with ```pip install -e .[test]```
3. Run tests via ```pytest``` or ```pytest-watch``` (short: ```ptw```)