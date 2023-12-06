Feature: Preprocessing
  
  Scenario: Preprocessing molecules
    Given a list of 10 random molecules, where 0 entries are None
    And an example model predicting molecular weight, version no_ids
    When the model preprocesses the molecules
    Then the preprocessed molecules are valid