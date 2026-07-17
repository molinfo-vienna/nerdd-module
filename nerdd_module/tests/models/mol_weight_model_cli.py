from nerdd_module import auto_cli

from .mol_weight_model import MolWeightModel


# we create a CLI for this model for testing
# it can be called using `python -m nerdd_module.tests.models.mol_weight_model_cli --help`
@auto_cli
def main() -> MolWeightModel:
    return MolWeightModel()


if __name__ == "__main__":
    main()
