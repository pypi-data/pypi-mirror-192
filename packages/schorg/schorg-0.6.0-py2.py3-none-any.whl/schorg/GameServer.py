"""
Server that provides game interaction in a multiplayer game.

https://schema.org/GameServer
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class GameServerInheritedProperties(TypedDict):
    """Server that provides game interaction in a multiplayer game.

    References:
        https://schema.org/GameServer
    Note:
        Model Depth 3
    Attributes:
    """

    


class GameServerProperties(TypedDict):
    """Server that provides game interaction in a multiplayer game.

    References:
        https://schema.org/GameServer
    Note:
        Model Depth 3
    Attributes:
        playersOnline: (Optional[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]): Number of players on the server.
        game: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Video game which is played on this server.
        serverStatus: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Status of a game server.
    """

    playersOnline: NotRequired[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]
    game: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    serverStatus: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#GameServerInheritedPropertiesTd = GameServerInheritedProperties()
#GameServerPropertiesTd = GameServerProperties()


class AllProperties(GameServerInheritedProperties , GameServerProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[GameServerProperties, GameServerInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "GameServer"
    return model
    

GameServer = create_schema_org_model()