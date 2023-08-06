"""
Auto body shop.

https://schema.org/AutoBodyShop
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AutoBodyShopInheritedProperties(TypedDict):
    """Auto body shop.

    References:
        https://schema.org/AutoBodyShop
    Note:
        Model Depth 5
    Attributes:
    """

    


class AutoBodyShopProperties(TypedDict):
    """Auto body shop.

    References:
        https://schema.org/AutoBodyShop
    Note:
        Model Depth 5
    Attributes:
    """

    

#AutoBodyShopInheritedPropertiesTd = AutoBodyShopInheritedProperties()
#AutoBodyShopPropertiesTd = AutoBodyShopProperties()


class AllProperties(AutoBodyShopInheritedProperties , AutoBodyShopProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AutoBodyShopProperties, AutoBodyShopInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "AutoBodyShop"
    return model
    

AutoBodyShop = create_schema_org_model()