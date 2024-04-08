Feature: Atom prediction

  Scenario Outline: Predicting a property for each atom
    Given a list of <num_molecules> random molecules, where <num_none> entries are None
    And the input type is '<input_type>'
    And the representations of the molecules
    And an example model predicting atomic masses, version <version>
    And a prediction parameter 'multiplier' set to <multiplier>

    When the model is used on the molecules given as <input_type>
    And the subset of the result where the input was not None is considered

    Then the result should be a pandas DataFrame
    And the result should contain as many rows as atoms in the input molecules
    And the result should contain the columns:
          mol_id
          name
          input_mol
          preprocessed_mol
          input_type
          errors
          atom_id
          mass
    And the input type column should be '<input_type>'
    And the name column should contain valid names
    And the mass column should contain the (multiplied) atomic masses
    And the input column should contain the input representation
    And the number of unique atom ids should be the same as the number of atoms in the input

    Examples:
    | input_type | version   | num_molecules | multiplier | num_none |
    | rdkit_mol  | no_ids    | 10            | 3          | 0        |
    | smiles     | no_ids    | 10            | 3          | 0        |
    | mol_block  | no_ids    | 10            | 3          | 0        |
    | rdkit_mol  | no_ids    | 10            | 3          | 5        |
    | smiles     | no_ids    | 10            | 3          | 5        |
    | mol_block  | no_ids    | 10            | 3          | 5        |
    | rdkit_mol  | no_ids    | 0             | 3          | 0        |
    | smiles     | no_ids    | 0             | 3          | 0        |
    | mol_block  | no_ids    | 0             | 3          | 0        |
    | rdkit_mol  | with_ids  | 10            | 3          | 0        |
    | smiles     | with_ids  | 10            | 3          | 0        |
    | mol_block  | with_ids  | 10            | 3          | 0        |
    | rdkit_mol  | with_ids  | 10            | 3          | 5        |
    | smiles     | with_ids  | 10            | 3          | 5        |
    | mol_block  | with_ids  | 10            | 3          | 5        |
    | rdkit_mol  | with_ids  | 0             | 3          | 0        |
    | smiles     | with_ids  | 0             | 3          | 0        |
    | mol_block  | with_ids  | 0             | 3          | 0        |
    | rdkit_mol  | with_mols | 10            | 3          | 0        |
    | smiles     | with_mols | 10            | 3          | 0        |
    | mol_block  | with_mols | 10            | 3          | 0        |
    | rdkit_mol  | with_mols | 10            | 3          | 5        |
    | smiles     | with_mols | 10            | 3          | 5        |
    | mol_block  | with_mols | 10            | 3          | 5        |
    | rdkit_mol  | with_mols | 0             | 3          | 0        |
    | smiles     | with_mols | 0             | 3          | 0        |
    | mol_block  | with_mols | 0             | 3          | 0        |