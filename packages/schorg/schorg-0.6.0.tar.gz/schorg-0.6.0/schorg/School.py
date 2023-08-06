"""
A school.

https://schema.org/School
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SchoolInheritedProperties(TypedDict):
    """A school.

    References:
        https://schema.org/School
    Note:
        Model Depth 4
    Attributes:
        alumni: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Alumni of an organization.
    """

    alumni: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class SchoolProperties(TypedDict):
    """A school.

    References:
        https://schema.org/School
    Note:
        Model Depth 4
    Attributes:
    """

    

#SchoolInheritedPropertiesTd = SchoolInheritedProperties()
#SchoolPropertiesTd = SchoolProperties()


class AllProperties(SchoolInheritedProperties , SchoolProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SchoolProperties, SchoolInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "School"
    return model
    

School = create_schema_org_model()