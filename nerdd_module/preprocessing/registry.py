from .chembl_structure_pipeline import ChemblStructurePipeline
from .empty_pipeline import EmptyPipeline
from .pipeline import Pipeline

__all__ = ["registry", "register_pipeline"]

registry = {}


def register_pipeline(pipeline: Pipeline):
    pipeline_name = pipeline.name
    registry[pipeline_name] = pipeline


register_pipeline(EmptyPipeline())

try:
    register_pipeline(ChemblStructurePipeline())
except ImportError:
    pass
