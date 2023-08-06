"""
A college, university, or other third-level educational institution.

https://schema.org/CollegeOrUniversity
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CollegeOrUniversityInheritedProperties(TypedDict):
    """A college, university, or other third-level educational institution.

    References:
        https://schema.org/CollegeOrUniversity
    Note:
        Model Depth 4
    Attributes:
        alumni: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Alumni of an organization.
    """

    alumni: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class CollegeOrUniversityProperties(TypedDict):
    """A college, university, or other third-level educational institution.

    References:
        https://schema.org/CollegeOrUniversity
    Note:
        Model Depth 4
    Attributes:
    """

    

#CollegeOrUniversityInheritedPropertiesTd = CollegeOrUniversityInheritedProperties()
#CollegeOrUniversityPropertiesTd = CollegeOrUniversityProperties()


class AllProperties(CollegeOrUniversityInheritedProperties , CollegeOrUniversityProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CollegeOrUniversityProperties, CollegeOrUniversityInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "CollegeOrUniversity"
    return model
    

CollegeOrUniversity = create_schema_org_model()