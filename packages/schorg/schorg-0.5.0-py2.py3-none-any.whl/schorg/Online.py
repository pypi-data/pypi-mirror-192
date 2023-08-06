"""
Game server status: Online. Server is available.

https://schema.org/Online
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OnlineInheritedProperties(TypedDict):
    """Game server status: Online. Server is available.

    References:
        https://schema.org/Online
    Note:
        Model Depth 6
    Attributes:
    """

    


class OnlineProperties(TypedDict):
    """Game server status: Online. Server is available.

    References:
        https://schema.org/Online
    Note:
        Model Depth 6
    Attributes:
    """

    

#OnlineInheritedPropertiesTd = OnlineInheritedProperties()
#OnlinePropertiesTd = OnlineProperties()


class AllProperties(OnlineInheritedProperties , OnlineProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OnlineProperties, OnlineInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Online"
    return model
    

Online = create_schema_org_model()