"""
A store that sells materials useful or necessary for various hobbies.

https://schema.org/HobbyShop
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class HobbyShopInheritedProperties(TypedDict):
    """A store that sells materials useful or necessary for various hobbies.

    References:
        https://schema.org/HobbyShop
    Note:
        Model Depth 5
    Attributes:
    """

    


class HobbyShopProperties(TypedDict):
    """A store that sells materials useful or necessary for various hobbies.

    References:
        https://schema.org/HobbyShop
    Note:
        Model Depth 5
    Attributes:
    """

    

#HobbyShopInheritedPropertiesTd = HobbyShopInheritedProperties()
#HobbyShopPropertiesTd = HobbyShopProperties()


class AllProperties(HobbyShopInheritedProperties , HobbyShopProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[HobbyShopProperties, HobbyShopInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "HobbyShop"
    return model
    

HobbyShop = create_schema_org_model()