Feature: Basic preprocessing functionality
  
  Scenario Outline: Preprocess molecules with an invalid preprocessing step
    Given an input molecule specified by '<input_smiles>'
    When the molecules are preprocessed by a dummy preprocessing step in mode 'error'
    And the subset of the result where the input was not None is considered
    Then the subset should contain the problem 'unknown_preprocessing_error'
    And the value in column 'preprocessed_mol' should be equal to None
    Examples:
    | input_smiles |
    | CI           |
    | C1CCCC1      |