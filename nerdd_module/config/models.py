from typing import Any, List, Optional, Union

from pydantic import BaseModel, model_validator

from ..polyfills import Literal


class Partner(BaseModel):
    name: str
    logo: str
    url: Optional[str] = None


class Author(BaseModel):
    """
    Author information

    Attributes:
        first_name : str
            First name of the author.
        last_name : str
            Last name of the author.
        email : Optional[str]
            Email of the author. If provided, the author is a corresponding author.
    """

    first_name: str
    last_name: str
    email: Optional[str] = None


class Publication(BaseModel):
    title: str
    authors: List[Author] = []
    journal: str
    year: int
    doi: Optional[str]


class JobParameterChoice(BaseModel):
    value: str
    label: Optional[str] = None


class JobParameter(BaseModel):
    name: str
    type: str
    visible_name: Optional[str] = None
    help_text: Optional[str] = None
    default: Any = None
    required: bool = False
    choices: Optional[List[JobParameterChoice]] = None


Task = Literal[
    "molecular_property_prediction",
    "atom_property_prediction",
    "derivative_property_prediction",
]
Level = Literal["molecule", "atom", "derivative"]

FormatSpec = Union[List[str], str]


class IncludeExcludeFormatSpec(BaseModel):
    include: Optional[FormatSpec]
    exclude: Optional[FormatSpec]


class ResultProperty(BaseModel):
    name: str
    type: str
    visible_name: Optional[str] = None
    help_text: Optional[str] = None
    sortable: bool = False
    group: Optional[str] = None
    level: Level = "molecule"
    formats: Union[FormatSpec, IncludeExcludeFormatSpec, None] = None
    representation: Optional[str] = None

    def is_visible(self, output_format: str) -> bool:
        formats = self.formats

        if formats is None:
            return True
        elif isinstance(formats, list):
            return output_format in formats
        elif isinstance(formats, IncludeExcludeFormatSpec):
            include = formats.include
            exclude = formats.exclude or []
            return (include is None or output_format in include) and output_format not in exclude
        else:
            raise ValueError(f"Invalid formats declaration {formats} in result property {self}")


class Module(BaseModel):
    task: Optional[Task] = None
    rank: Optional[int] = None
    name: Optional[str] = None
    batch_size: int = 100
    version: Optional[str] = None
    visible_name: Optional[str] = None
    logo: Optional[str] = None
    logo_title: Optional[str] = None
    logo_caption: Optional[str] = None
    example_smiles: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    partners: List[Partner] = []
    publications: List[Publication] = []
    about: Optional[str] = None
    job_parameters: List[JobParameter] = []
    result_properties: List[ResultProperty] = []

    def get_property_columns_of_type(self, t: Level) -> List[ResultProperty]:
        return [c for c in self.result_properties if c.level == t]

    def molecular_property_columns(self) -> List[ResultProperty]:
        return self.get_property_columns_of_type("molecule")

    def atom_property_columns(self) -> List[ResultProperty]:
        return self.get_property_columns_of_type("atom")

    def derivative_property_columns(self) -> List[ResultProperty]:
        return self.get_property_columns_of_type("derivative")

    def get_visible_properties(self, output_format: str) -> List[ResultProperty]:
        return [p for p in self.result_properties if p.is_visible(output_format)]

    @model_validator(mode="after")
    @classmethod
    def validate_model(cls, values: Any) -> Any:
        assert isinstance(values, Module)

        num_atom_properties = len(values.get_property_columns_of_type("atom"))
        num_derivative_properties = len(values.get_property_columns_of_type("derivative"))
        task = values.task
        if task is None:
            # if task is not specified, try to derive it from the result_properties
            if num_atom_properties > 0:
                task = "atom_property_prediction"
            elif num_derivative_properties > 0:
                task = "derivative_property_prediction"
            else:
                task = "molecular_property_prediction"

            values.task = task
        else:
            # if task is specified, check if it is consistent with the result_properties
            if num_atom_properties > 0:
                assert (
                    task == "atom_property_prediction"
                ), "Task should be atom_property_prediction if atom properties are present."
            elif num_derivative_properties > 0:
                assert task == "derivative_property_prediction", (
                    "Task should be derivative_property_prediction if derivative properties "
                    "are present."
                )
            else:
                assert task == "molecular_property_prediction", (
                    "Task should be molecular_property_prediction if no atom or derivative "
                    "properties are present."
                )

        # check that a module can only predict atom or derivative properties, not both
        assert (
            num_atom_properties == 0 or num_derivative_properties == 0
        ), "A module can only predict atom or derivative properties, not both."

        # check that two properties with the same group appear next to each other
        groups = [p.group for p in values.result_properties if p.group is not None]
        for group in groups:
            indices = [i for i, p in enumerate(values.result_properties) if p.group == group]
            for i, j in zip(indices[:-1], indices[1:]):
                assert i + 1 == j, (
                    f"Properties with the same group should appear next to each other, "
                    f"but group {group} appears at incides {i} and {j}."
                )

        return values
