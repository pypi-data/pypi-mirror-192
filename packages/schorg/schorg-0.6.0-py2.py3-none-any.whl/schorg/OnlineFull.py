"""
Game server status: OnlineFull. Server is online but unavailable. The maximum number of players has reached.

https://schema.org/OnlineFull
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OnlineFullInheritedProperties(TypedDict):
    """Game server status: OnlineFull. Server is online but unavailable. The maximum number of players has reached.

    References:
        https://schema.org/OnlineFull
    Note:
        Model Depth 6
    Attributes:
    """

    


class OnlineFullProperties(TypedDict):
    """Game server status: OnlineFull. Server is online but unavailable. The maximum number of players has reached.

    References:
        https://schema.org/OnlineFull
    Note:
        Model Depth 6
    Attributes:
    """

    

#OnlineFullInheritedPropertiesTd = OnlineFullInheritedProperties()
#OnlineFullPropertiesTd = OnlineFullProperties()


class AllProperties(OnlineFullInheritedProperties , OnlineFullProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OnlineFullProperties, OnlineFullInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OnlineFull"
    return model
    

OnlineFull = create_schema_org_model()