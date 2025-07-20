from rdkit.Chem import MolFromSmiles

from nerdd_module import Model

example_molecules = [
    MolFromSmiles("CCO"),
    MolFromSmiles("CCN"),
]


class ModelUsingPropertyTypeSynonyms(Model):
    def __init__(self):
        super().__init__()

    def _predict_mols(self, mols):
        return [
            {
                "mol_id": 0,
                "p1": 3,
                "p2": 3,
                "p3": 3.1,
                "p4": "test",
                "p5": "test",
                "p6": False,
                "p7": False,
            },
            {
                "mol_id": 1,
                "p1": 4,
                "p2": 4,
                "p3": 4.2,
                "p4": "example",
                "p5": "example",
                "p6": True,
                "p7": True,
            },
        ]

    def _get_base_config(self):
        return {
            "result_properties": [
                {
                    "name": "p1",
                    "type": "integer",
                },
                {
                    "name": "p2",
                    "type": "int",
                },
                {
                    "name": "p3",
                    "type": "float",
                },
                {
                    "name": "p4",
                    "type": "string",
                },
                {
                    "name": "p5",
                    "type": "str",
                },
                {
                    "name": "p6",
                    "type": "boolean",
                },
                {
                    "name": "p7",
                    "type": "bool",
                },
            ]
        }


def test_basic_types_synonyms():
    model = ModelUsingPropertyTypeSynonyms()

    results = model.predict(example_molecules, output_format="record_list")

    # check types
    for r in results:
        assert isinstance(r["p1"], int)
        assert isinstance(r["p2"], int)
        assert isinstance(r["p3"], float)
        assert isinstance(r["p4"], str)
        assert isinstance(r["p5"], str)
        assert isinstance(r["p6"], bool)
        assert isinstance(r["p7"], bool)
