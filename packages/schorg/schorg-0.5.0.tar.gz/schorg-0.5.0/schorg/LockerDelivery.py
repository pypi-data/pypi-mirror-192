"""
A DeliveryMethod in which an item is made available via locker.

https://schema.org/LockerDelivery
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class LockerDeliveryInheritedProperties(TypedDict):
    """A DeliveryMethod in which an item is made available via locker.

    References:
        https://schema.org/LockerDelivery
    Note:
        Model Depth 5
    Attributes:
    """

    


class LockerDeliveryProperties(TypedDict):
    """A DeliveryMethod in which an item is made available via locker.

    References:
        https://schema.org/LockerDelivery
    Note:
        Model Depth 5
    Attributes:
    """

    

#LockerDeliveryInheritedPropertiesTd = LockerDeliveryInheritedProperties()
#LockerDeliveryPropertiesTd = LockerDeliveryProperties()


class AllProperties(LockerDeliveryInheritedProperties , LockerDeliveryProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[LockerDeliveryProperties, LockerDeliveryInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "LockerDelivery"
    return model
    

LockerDelivery = create_schema_org_model()