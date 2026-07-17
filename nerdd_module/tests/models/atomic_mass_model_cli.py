from nerdd_module import auto_cli

from .atomic_mass_model import AtomicMassModel


# we create a CLI for this model for testing
# it can be called using `python -m nerdd_module.tests.models.atomic_mass_model_cli --help`
@auto_cli
def main() -> AtomicMassModel:
    return AtomicMassModel()


if __name__ == "__main__":
    main()
