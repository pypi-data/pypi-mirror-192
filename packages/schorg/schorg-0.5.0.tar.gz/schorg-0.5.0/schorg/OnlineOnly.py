"""
Indicates that the item is available only online.

https://schema.org/OnlineOnly
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OnlineOnlyInheritedProperties(TypedDict):
    """Indicates that the item is available only online.

    References:
        https://schema.org/OnlineOnly
    Note:
        Model Depth 5
    Attributes:
    """

    


class OnlineOnlyProperties(TypedDict):
    """Indicates that the item is available only online.

    References:
        https://schema.org/OnlineOnly
    Note:
        Model Depth 5
    Attributes:
    """

    

#OnlineOnlyInheritedPropertiesTd = OnlineOnlyInheritedProperties()
#OnlineOnlyPropertiesTd = OnlineOnlyProperties()


class AllProperties(OnlineOnlyInheritedProperties , OnlineOnlyProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OnlineOnlyProperties, OnlineOnlyInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OnlineOnly"
    return model
    

OnlineOnly = create_schema_org_model()