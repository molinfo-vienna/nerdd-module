Feature: Filter small fragments

  Scenario Outline: Keep largest fragment
    Given an input molecule specified by '<input_smiles>'
    When small fragments are removed from the molecules
    And all results are considered
    Then the value in column 'preprocessed_mol' should not be equal to None
    And the value in column 'preprocessed_smiles' should be equal to '<expected_smiles>'
    Examples:
    | input_smiles | expected_smiles |
    | CC           | CC              |
    | CC.C         | CC              |
    | [H][H]       | [H][H]          |
    | CC.CC        | CC              |
    | C1CCCCC1     | C1CCCCC1        |