Feature: Remove hydrogens
  
  Scenario Outline: Remove hydrogens in normal molecules
    Given an input molecule specified by '<input_smiles>'
    When hydrogens are removed
    And the subset of the result where the input was not None is considered
    Then the value in column 'preprocessed_mol' should not be equal to None
    And the value in column 'preprocessed_smiles' should be equal to '<expected_smiles>'
    Examples:
    | input_smiles           | expected_smiles |
    | CC                     | CC              |
    | [CH4].CC               | C.CC            |
    | [H][H]                 | [H][H]          |
    | [CH3]C                 | CC              |
    | C1CCCC([H])([H])C1     | C1CCCCC1        |