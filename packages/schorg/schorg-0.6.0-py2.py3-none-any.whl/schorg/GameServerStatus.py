"""
Status of a game server.

https://schema.org/GameServerStatus
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class GameServerStatusInheritedProperties(TypedDict):
    """Status of a game server.

    References:
        https://schema.org/GameServerStatus
    Note:
        Model Depth 5
    Attributes:
    """

    


class GameServerStatusProperties(TypedDict):
    """Status of a game server.

    References:
        https://schema.org/GameServerStatus
    Note:
        Model Depth 5
    Attributes:
    """

    

#GameServerStatusInheritedPropertiesTd = GameServerStatusInheritedProperties()
#GameServerStatusPropertiesTd = GameServerStatusProperties()


class AllProperties(GameServerStatusInheritedProperties , GameServerStatusProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[GameServerStatusProperties, GameServerStatusInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "GameServerStatus"
    return model
    

GameServerStatus = create_schema_org_model()