"""
An office equipment store.

https://schema.org/OfficeEquipmentStore
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OfficeEquipmentStoreInheritedProperties(TypedDict):
    """An office equipment store.

    References:
        https://schema.org/OfficeEquipmentStore
    Note:
        Model Depth 5
    Attributes:
    """

    


class OfficeEquipmentStoreProperties(TypedDict):
    """An office equipment store.

    References:
        https://schema.org/OfficeEquipmentStore
    Note:
        Model Depth 5
    Attributes:
    """

    

#OfficeEquipmentStoreInheritedPropertiesTd = OfficeEquipmentStoreInheritedProperties()
#OfficeEquipmentStorePropertiesTd = OfficeEquipmentStoreProperties()


class AllProperties(OfficeEquipmentStoreInheritedProperties , OfficeEquipmentStoreProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OfficeEquipmentStoreProperties, OfficeEquipmentStoreInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OfficeEquipmentStore"
    return model
    

OfficeEquipmentStore = create_schema_org_model()