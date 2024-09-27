Feature: Filter molecules by weight
  
  Scenario Outline: Tag molecules with invalid weight
    Given an input molecule specified by '<input_smiles>'
    When the molecules are filtered by weight (range=[100, 1000], remove_invalid_molecules=False)
    And the subset of the result where the input was not None is considered
    Then the subset should contain the problem 'invalid_weight'
    And the value in column 'preprocessed_mol' should not be equal to None
    Examples:
    | input_smiles |
    | CF           |
    | c1ccccc1     |
    | [H][H]       |

  Scenario Outline: Do not tag molecules having a valid weight
    Given an input molecule specified by '<input_smiles>'
    When the molecules are filtered by weight (range=[100, 1000], remove_invalid_molecules=False)
    And the subset of the result where the input was not None is considered
    Then the subset should not contain the problem 'invalid_weight'
    And the value in column 'preprocessed_mol' should not be equal to None
    Examples:
    | input_smiles |
    | CI           |
    | CCCCCCCCCC   |

  Scenario Outline: Setting remove_invalid_molecules to True
    Given an input molecule specified by '<input_smiles>'
    When the molecules are filtered by weight (range=[100, 1000], remove_invalid_molecules=True)
    And the subset of the result where the input was not None is considered
    Then the subset should contain the problem 'invalid_weight'
    And the value in column 'preprocessed_mol' should be equal to None
    Examples:
    | input_smiles |
    | CF           |
    | c1ccccc1     |
    | [H][H]       |