from typing import List, Literal, Optional

from pydantic import BaseModel


class Partner(BaseModel):
    name: str
    logo: str
    url: Optional[str]


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
    email: Optional[str]


class Publication(BaseModel):
    title: str
    authors: List[Author]
    journal: str
    year: str
    doi: Optional[str]


class JobParameter(BaseModel):
    name: str
    type: str
    visible_name: str
    help_text: Optional[str]
    default: Optional[str]
    required: bool = False


class ResultProperty(BaseModel):
    name: str
    type: str
    visible_name: str
    help_text: Optional[str]
    sortable: bool = False
    group: Optional[str]


class Module(BaseModel):
    task: Literal[
        "molecular_property_prediction",
        "atom_property_prediction",
        "derivative_property_prediction",
    ] = "molecular_property_prediction"
    rank: Optional[int]
    name: Optional[str]
    visible_name: Optional[str]
    logo: Optional[str]
    logo_title: Optional[str]
    logo_caption: Optional[str]
    example_smiles: Optional[str]
    title: Optional[str]
    description: Optional[str]
    partners: List[Partner] = []
    publications: List[Publication] = []
    about: Optional[str]
    job_parameters: List[JobParameter] = []
    result_properties: List[ResultProperty] = []
