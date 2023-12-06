from .pipeline import Pipeline

__all__ = ["EmptyPipeline"]


class EmptyPipeline(Pipeline):
    def __init__(self):
        super().__init__(steps=[], name="no_preprocessing")
