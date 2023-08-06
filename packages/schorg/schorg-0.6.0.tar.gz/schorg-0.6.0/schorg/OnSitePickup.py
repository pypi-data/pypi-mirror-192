"""
A DeliveryMethod in which an item is collected on site, e.g. in a store or at a box office.

https://schema.org/OnSitePickup
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OnSitePickupInheritedProperties(TypedDict):
    """A DeliveryMethod in which an item is collected on site, e.g. in a store or at a box office.

    References:
        https://schema.org/OnSitePickup
    Note:
        Model Depth 5
    Attributes:
    """

    


class OnSitePickupProperties(TypedDict):
    """A DeliveryMethod in which an item is collected on site, e.g. in a store or at a box office.

    References:
        https://schema.org/OnSitePickup
    Note:
        Model Depth 5
    Attributes:
    """

    

#OnSitePickupInheritedPropertiesTd = OnSitePickupInheritedProperties()
#OnSitePickupPropertiesTd = OnSitePickupProperties()


class AllProperties(OnSitePickupInheritedProperties , OnSitePickupProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OnSitePickupProperties, OnSitePickupInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OnSitePickup"
    return model
    

OnSitePickup = create_schema_org_model()