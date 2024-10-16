Feature: Reading molecule representations

  Scenario Outline: Read a single molecule from a valid representation

    Given a list of 1 random molecules, where 0 entries are None
    And the input type is '<input_type>'
    And the representations of the molecules
    When the reader gets the representations as input with input type <input_type>
    Then the result should contain the same number of entries as the input
    And the result should contain the same number of non-null entries as the input

    Examples:
    | input_type |
    | rdkit_mol  |
    | smiles     |
    | mol_block  |
    | inchi      |

  Scenario Outline: Read lists of molecules from valid representations

    Given a list of <num_molecules> random molecules, where <num_none> entries are None
    And the input type is '<input_type>'
    And the representations of the molecules
    When the reader gets the representations as input with input type <input_type>
    Then the result should contain the same number of entries as the input

    Examples:
    | input_type | num_molecules | num_none |
    | rdkit_mol  | 0             | 0        |
    | smiles     | 10            | 0        |
    | mol_block  | 10            | 0        |
    | inchi      | 10            | 0        |
    | rdkit_mol  | 10            | 0        |
    | smiles     | 10            | 5        |
    | mol_block  | 10            | 5        |
    | inchi      | 10            | 5        |
    | rdkit_mol  | 10            | 5        |
    | smiles     | 10            | 9        |
    | mol_block  | 10            | 9        |
    | inchi      | 10            | 9        |
    | rdkit_mol  | 10            | 9        |
    
  Scenario Outline: Read a single file containing valid representations

    Given a list of <num_molecules> random molecules, where <num_none> entries are None
    And the input type is '<input_type>'
    And the representations of the molecules
    And a file containing the representations
    When the reader gets the file name(s) as input
    Then the result should contain the same number of entries as the input

    Examples:
    | input_type | num_molecules | num_none |
    | smiles     | 10            | 0        |
    | mol_block  | 10            | 0        |
    | inchi      | 10            | 0        |
    | smiles     | 10            | 5        |
    | mol_block  | 10            | 5        |
    | inchi      | 10            | 5        |


  Scenario Outline: Read multiple files containing valid representations

    Given a list of <num_molecules> random molecules, where <num_none> entries are None
    And the input type is '<input_type>'
    And the representations of the molecules
    And a list of <num_files> files containing the representations
    When the reader gets the file name(s) as input
    Then the result should contain the same number of entries as the input
    And the source of each entry should be one of the file names

    Examples:
    | input_type | num_molecules  | num_none | num_files |
    | smiles     | 10             | 0        | 1         |
    | mol_block  | 10             | 0        | 1         |
    | inchi      | 10             | 0        | 1         |
    | smiles     | 10             | 5        | 1         |
    | mol_block  | 10             | 5        | 1         |
    | inchi      | 10             | 5        | 1         |
    | smiles     | 100            | 0        | 10        |
    | mol_block  | 100            | 0        | 10        |
    | smiles     | 100            | 5        | 10        |
    | mol_block  | 100            | 5        | 10        |
    | smiles     | 100            | 9        | 10        |
    | mol_block  | 100            | 9        | 10        |
  