"""
An outlet store.

https://schema.org/OutletStore
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OutletStoreInheritedProperties(TypedDict):
    """An outlet store.

    References:
        https://schema.org/OutletStore
    Note:
        Model Depth 5
    Attributes:
    """

    


class OutletStoreProperties(TypedDict):
    """An outlet store.

    References:
        https://schema.org/OutletStore
    Note:
        Model Depth 5
    Attributes:
    """

    

#OutletStoreInheritedPropertiesTd = OutletStoreInheritedProperties()
#OutletStorePropertiesTd = OutletStoreProperties()


class AllProperties(OutletStoreInheritedProperties , OutletStoreProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OutletStoreProperties, OutletStoreInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OutletStore"
    return model
    

OutletStore = create_schema_org_model()