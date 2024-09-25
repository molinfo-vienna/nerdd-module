Feature: Filter molecules by element
  
  Scenario Outline: Tag molecules with invalid elements
    Given an input molecule specified by '<input_smiles>'
    And the list of allowed elements is ['C', 'H', 'O', 'N']
    And the parameter remove_invalid_molecules is set to False
    When the molecules are filtered by element
    And the subset of the result where the input was not None is considered
    Then the subset should contain the problem 'invalid_elements'
    And the value in column 'preprocessed_mol' should not be equal to None
    Examples:
    | input_smiles |
    | CI           |

  Scenario Outline: Do not tag molecules having only allowed elements
    Given an input molecule specified by '<input_smiles>'
    And the list of allowed elements is ['C', 'H', 'O', 'N']
    And the parameter remove_invalid_molecules is set to False
    When the molecules are filtered by element
    And the subset of the result where the input was not None is considered
    Then the subset should not contain the problem 'invalid_elements'
    And the value in column 'preprocessed_mol' should not be equal to None
    Examples:
    | input_smiles |
    | CCO          |
    | [H][H]       |


  Scenario Outline: Filter molecules containing hydrogen
    Given an input molecule specified by '<input_smiles>'
    And the list of allowed elements is ['C', 'O', 'N']
    And the parameter remove_invalid_molecules is set to False
    When the molecules are filtered by element
    And the subset of the result where the input was not None is considered
    Then the subset should contain the problem 'invalid_elements'
    And the value in column 'preprocessed_mol' should not be equal to None
    Examples:
    | input_smiles |
    | CCO          |
    | [H][H]       |


  Scenario Outline: Setting allowed elements to an empty list
    Given an input molecule specified by '<input_smiles>'
    And the list of allowed elements is []
    And the parameter remove_invalid_molecules is set to False
    When the molecules are filtered by element
    And the subset of the result where the input was not None is considered
    Then the subset should contain the problem 'invalid_elements'
    And the value in column 'preprocessed_mol' should not be equal to None
    Examples:
    | input_smiles |
    | CCO          |
    | [H][H]       |
    | O=O          |

  Scenario Outline: Setting remove_invalid_molecules to True
    Given an input molecule specified by '<input_smiles>'
    And the list of allowed elements is ['C', 'O', 'H']
    And the parameter remove_invalid_molecules is set to True
    When the molecules are filtered by element
    And the subset of the result where the input was not None is considered
    Then the subset should contain the problem 'invalid_elements'
    And the value in column 'preprocessed_mol' should be equal to None
    Examples:
    | input_smiles |
    | CCCCCS       |

  Scenario Outline: Using lowercase element symbols also works
    Given an input molecule specified by '<input_smiles>'
    And the list of allowed elements is ['c', 'h', 'o', 'n']
    And the parameter remove_invalid_molecules is set to False
    When the molecules are filtered by element
    And the subset of the result where the input was not None is considered
    Then the subset should not contain the problem 'invalid_elements'
    And the value in column 'preprocessed_mol' should not be equal to None
    Examples:
    | input_smiles |
    | CCO          |
    | [H][H]       |