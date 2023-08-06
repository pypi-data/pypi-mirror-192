"""
A jewelry store.

https://schema.org/JewelryStore
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class JewelryStoreInheritedProperties(TypedDict):
    """A jewelry store.

    References:
        https://schema.org/JewelryStore
    Note:
        Model Depth 5
    Attributes:
    """

    


class JewelryStoreProperties(TypedDict):
    """A jewelry store.

    References:
        https://schema.org/JewelryStore
    Note:
        Model Depth 5
    Attributes:
    """

    

#JewelryStoreInheritedPropertiesTd = JewelryStoreInheritedProperties()
#JewelryStorePropertiesTd = JewelryStoreProperties()


class AllProperties(JewelryStoreInheritedProperties , JewelryStoreProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[JewelryStoreProperties, JewelryStoreInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "JewelryStore"
    return model
    

JewelryStore = create_schema_org_model()