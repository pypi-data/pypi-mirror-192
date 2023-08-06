"""
A system of medicine focused on the relationship between the body's structure, mainly the spine, and its functioning.

https://schema.org/Chiropractic
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ChiropracticInheritedProperties(TypedDict):
    """A system of medicine focused on the relationship between the body's structure, mainly the spine, and its functioning.

    References:
        https://schema.org/Chiropractic
    Note:
        Model Depth 6
    Attributes:
    """

    


class ChiropracticProperties(TypedDict):
    """A system of medicine focused on the relationship between the body's structure, mainly the spine, and its functioning.

    References:
        https://schema.org/Chiropractic
    Note:
        Model Depth 6
    Attributes:
    """

    

#ChiropracticInheritedPropertiesTd = ChiropracticInheritedProperties()
#ChiropracticPropertiesTd = ChiropracticProperties()


class AllProperties(ChiropracticInheritedProperties , ChiropracticProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ChiropracticProperties, ChiropracticInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Chiropractic"
    return model
    

Chiropractic = create_schema_org_model()