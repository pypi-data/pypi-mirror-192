"""
Indicates that the item has been discontinued.

https://schema.org/Discontinued
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DiscontinuedInheritedProperties(TypedDict):
    """Indicates that the item has been discontinued.

    References:
        https://schema.org/Discontinued
    Note:
        Model Depth 5
    Attributes:
    """

    


class DiscontinuedProperties(TypedDict):
    """Indicates that the item has been discontinued.

    References:
        https://schema.org/Discontinued
    Note:
        Model Depth 5
    Attributes:
    """

    

#DiscontinuedInheritedPropertiesTd = DiscontinuedInheritedProperties()
#DiscontinuedPropertiesTd = DiscontinuedProperties()


class AllProperties(DiscontinuedInheritedProperties , DiscontinuedProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DiscontinuedProperties, DiscontinuedInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Discontinued"
    return model
    

Discontinued = create_schema_org_model()