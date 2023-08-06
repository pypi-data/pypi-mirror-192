"""
A hardware store.

https://schema.org/HardwareStore
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class HardwareStoreInheritedProperties(TypedDict):
    """A hardware store.

    References:
        https://schema.org/HardwareStore
    Note:
        Model Depth 5
    Attributes:
    """

    


class HardwareStoreProperties(TypedDict):
    """A hardware store.

    References:
        https://schema.org/HardwareStore
    Note:
        Model Depth 5
    Attributes:
    """

    

#HardwareStoreInheritedPropertiesTd = HardwareStoreInheritedProperties()
#HardwareStorePropertiesTd = HardwareStoreProperties()


class AllProperties(HardwareStoreInheritedProperties , HardwareStoreProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[HardwareStoreProperties, HardwareStoreInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "HardwareStore"
    return model
    

HardwareStore = create_schema_org_model()