"""
A men's clothing store.

https://schema.org/MensClothingStore
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MensClothingStoreInheritedProperties(TypedDict):
    """A men's clothing store.

    References:
        https://schema.org/MensClothingStore
    Note:
        Model Depth 5
    Attributes:
    """

    


class MensClothingStoreProperties(TypedDict):
    """A men's clothing store.

    References:
        https://schema.org/MensClothingStore
    Note:
        Model Depth 5
    Attributes:
    """

    

#MensClothingStoreInheritedPropertiesTd = MensClothingStoreInheritedProperties()
#MensClothingStorePropertiesTd = MensClothingStoreProperties()


class AllProperties(MensClothingStoreInheritedProperties , MensClothingStoreProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MensClothingStoreProperties, MensClothingStoreInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MensClothingStore"
    return model
    

MensClothingStore = create_schema_org_model()