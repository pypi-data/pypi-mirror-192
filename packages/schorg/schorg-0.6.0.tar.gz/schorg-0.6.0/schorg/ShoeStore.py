"""
A shoe store.

https://schema.org/ShoeStore
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ShoeStoreInheritedProperties(TypedDict):
    """A shoe store.

    References:
        https://schema.org/ShoeStore
    Note:
        Model Depth 5
    Attributes:
    """

    


class ShoeStoreProperties(TypedDict):
    """A shoe store.

    References:
        https://schema.org/ShoeStore
    Note:
        Model Depth 5
    Attributes:
    """

    

#ShoeStoreInheritedPropertiesTd = ShoeStoreInheritedProperties()
#ShoeStorePropertiesTd = ShoeStoreProperties()


class AllProperties(ShoeStoreInheritedProperties , ShoeStoreProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ShoeStoreProperties, ShoeStoreInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ShoeStore"
    return model
    

ShoeStore = create_schema_org_model()