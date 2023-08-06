"""
A high school.

https://schema.org/HighSchool
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class HighSchoolInheritedProperties(TypedDict):
    """A high school.

    References:
        https://schema.org/HighSchool
    Note:
        Model Depth 4
    Attributes:
        alumni: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Alumni of an organization.
    """

    alumni: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class HighSchoolProperties(TypedDict):
    """A high school.

    References:
        https://schema.org/HighSchool
    Note:
        Model Depth 4
    Attributes:
    """

    

#HighSchoolInheritedPropertiesTd = HighSchoolInheritedProperties()
#HighSchoolPropertiesTd = HighSchoolProperties()


class AllProperties(HighSchoolInheritedProperties , HighSchoolProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[HighSchoolProperties, HighSchoolInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "HighSchool"
    return model
    

HighSchool = create_schema_org_model()