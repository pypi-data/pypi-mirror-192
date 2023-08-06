"""
Indicates that the item has sold out.

https://schema.org/SoldOut
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SoldOutInheritedProperties(TypedDict):
    """Indicates that the item has sold out.

    References:
        https://schema.org/SoldOut
    Note:
        Model Depth 5
    Attributes:
    """

    


class SoldOutProperties(TypedDict):
    """Indicates that the item has sold out.

    References:
        https://schema.org/SoldOut
    Note:
        Model Depth 5
    Attributes:
    """

    

#SoldOutInheritedPropertiesTd = SoldOutInheritedProperties()
#SoldOutPropertiesTd = SoldOutProperties()


class AllProperties(SoldOutInheritedProperties , SoldOutProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SoldOutProperties, SoldOutInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "SoldOut"
    return model
    

SoldOut = create_schema_org_model()