Feature: Atom property prediction

  Scenario Outline: Predicting a property for each atom
    Given a list of <num_molecules> random molecules, where <num_none> entries are None
    And the input type is '<input_type>'
    And the representations of the molecules
    And a prediction parameter 'multiplier' set to <multiplier>

    When the atomic mass model (version '<version>') generates predictions for the molecule representations
    And the subset of the result where the input was not None is considered

    Then the result should contain as many rows as atoms in the input molecules
    And the result should contain the columns:
          mol_id
          name
          input_mol
          preprocessed_mol
          input_type
          problems
          atom_id
          mass
    And the value in column 'input_type' should be equal to '<input_type>'
    And the value in column 'name' should not be equal to None
    And the value in column 'mass' should be between 0 and infinity
    And the number of unique atom ids should be the same as the number of atoms in the input
    And the problems column should be a list of problem instances

    Examples:
    | input_type | version   | num_molecules | multiplier | num_none |
    | rdkit_mol  | mol_ids   | 10            | 3          | 0        |
    | smiles     | mol_ids   | 10            | 3          | 0        |
    | mol_block  | mol_ids   | 10            | 3          | 0        |
    | rdkit_mol  | mol_ids   | 10            | 3          | 5        |
    | smiles     | mol_ids   | 10            | 3          | 5        |
    | mol_block  | mol_ids   | 10            | 3          | 5        |
    | rdkit_mol  | mol_ids   | 0             | 3          | 0        |
    | smiles     | mol_ids   | 0             | 3          | 0        |
    | mol_block  | mol_ids   | 0             | 3          | 0        |
    | rdkit_mol  | mols      | 10            | 3          | 0        |
    | smiles     | mols      | 10            | 3          | 0        |
    | mol_block  | mols      | 10            | 3          | 0        |
    | rdkit_mol  | mols      | 10            | 3          | 5        |
    | smiles     | mols      | 10            | 3          | 5        |
    | mol_block  | mols      | 10            | 3          | 5        |
    | rdkit_mol  | mols      | 0             | 3          | 0        |
    | smiles     | mols      | 0             | 3          | 0        |
    | mol_block  | mols      | 0             | 3          | 0        |
    | rdkit_mol  | iterator  | 10            | 3          | 0        |
    | smiles     | iterator  | 10            | 3          | 0        |
    | mol_block  | iterator  | 10            | 3          | 0        |
    | rdkit_mol  | iterator  | 10            | 3          | 5        |
    | smiles     | iterator  | 10            | 3          | 5        |
    | mol_block  | iterator  | 10            | 3          | 5        |
    | rdkit_mol  | iterator  | 0             | 3          | 0        |
    | smiles     | iterator  | 0             | 3          | 0        |
    | mol_block  | iterator  | 0             | 3          | 0        |


Scenario: Predicting a property for each atom with an invalid model
    Given a list of 10 random molecules, where 0 entries are None
    And the input type is 'rdkit_mol'
    And the representations of the molecules
    And a prediction parameter 'multiplier' set to 10

    When the atomic mass model (version 'error') generates predictions for the molecule representations
    
    Then the result should contain the same number of rows as the input
    And the result should contain the columns:
          mol_id
          name
          input_mol
          preprocessed_mol
          input_type
          problems
          atom_id
          mass
    And the problems column should be a list of problem instances