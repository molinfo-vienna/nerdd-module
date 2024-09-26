Feature: Standardize with Chembl Structure Pipeline
  
  Scenario Outline: Preprocess normal molecules
    Given an input molecule specified by '<input_smiles>'
    When small fragments are removed from the molecules with CSP
    And the subset of the result where the input was not None is considered
    Then the value in column 'preprocessed_mol' should not be equal to None
    Examples:
    | input_smiles |
    | CI           |
    | C1CCCC1      |