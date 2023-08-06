"""
VinylFormat.

https://schema.org/VinylFormat
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class VinylFormatInheritedProperties(TypedDict):
    """VinylFormat.

    References:
        https://schema.org/VinylFormat
    Note:
        Model Depth 5
    Attributes:
    """

    


class VinylFormatProperties(TypedDict):
    """VinylFormat.

    References:
        https://schema.org/VinylFormat
    Note:
        Model Depth 5
    Attributes:
    """

    

#VinylFormatInheritedPropertiesTd = VinylFormatInheritedProperties()
#VinylFormatPropertiesTd = VinylFormatProperties()


class AllProperties(VinylFormatInheritedProperties , VinylFormatProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[VinylFormatProperties, VinylFormatInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "VinylFormat"
    return model
    

VinylFormat = create_schema_org_model()