"""
A specific branch of medical science that is concerned with the diagnosis and treatment of diseases pertaining to the urinary tract and the urogenital system.

https://schema.org/Urologic
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class UrologicInheritedProperties(TypedDict):
    """A specific branch of medical science that is concerned with the diagnosis and treatment of diseases pertaining to the urinary tract and the urogenital system.

    References:
        https://schema.org/Urologic
    Note:
        Model Depth 6
    Attributes:
    """

    


class UrologicProperties(TypedDict):
    """A specific branch of medical science that is concerned with the diagnosis and treatment of diseases pertaining to the urinary tract and the urogenital system.

    References:
        https://schema.org/Urologic
    Note:
        Model Depth 6
    Attributes:
    """

    

#UrologicInheritedPropertiesTd = UrologicInheritedProperties()
#UrologicPropertiesTd = UrologicProperties()


class AllProperties(UrologicInheritedProperties , UrologicProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[UrologicProperties, UrologicInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Urologic"
    return model
    

Urologic = create_schema_org_model()