"""
An auto parts store.

https://schema.org/AutoPartsStore
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AutoPartsStoreInheritedProperties(TypedDict):
    """An auto parts store.

    References:
        https://schema.org/AutoPartsStore
    Note:
        Model Depth 5
    Attributes:
    """

    


class AutoPartsStoreProperties(TypedDict):
    """An auto parts store.

    References:
        https://schema.org/AutoPartsStore
    Note:
        Model Depth 5
    Attributes:
    """

    

#AutoPartsStoreInheritedPropertiesTd = AutoPartsStoreInheritedProperties()
#AutoPartsStorePropertiesTd = AutoPartsStoreProperties()


class AllProperties(AutoPartsStoreInheritedProperties , AutoPartsStoreProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AutoPartsStoreProperties, AutoPartsStoreInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "AutoPartsStore"
    return model
    

AutoPartsStore = create_schema_org_model()