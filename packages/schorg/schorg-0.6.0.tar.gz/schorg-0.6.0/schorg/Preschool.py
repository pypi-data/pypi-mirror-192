"""
A preschool.

https://schema.org/Preschool
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PreschoolInheritedProperties(TypedDict):
    """A preschool.

    References:
        https://schema.org/Preschool
    Note:
        Model Depth 4
    Attributes:
        alumni: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Alumni of an organization.
    """

    alumni: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class PreschoolProperties(TypedDict):
    """A preschool.

    References:
        https://schema.org/Preschool
    Note:
        Model Depth 4
    Attributes:
    """

    

#PreschoolInheritedPropertiesTd = PreschoolInheritedProperties()
#PreschoolPropertiesTd = PreschoolProperties()


class AllProperties(PreschoolInheritedProperties , PreschoolProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PreschoolProperties, PreschoolInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Preschool"
    return model
    

Preschool = create_schema_org_model()