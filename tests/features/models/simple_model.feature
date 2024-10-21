Feature: Simple model

  Scenario Outline: Simple model provides required attributes
    Given the mol weight model (version 'mols')

    Then the model should have attribute 'name' with value 'mol_scale'
    And the model should have attribute 'description' with value 'Computes the molecular weight of a molecule'

