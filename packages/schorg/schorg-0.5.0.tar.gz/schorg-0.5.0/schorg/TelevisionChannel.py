"""
A unique instance of a television BroadcastService on a CableOrSatelliteService lineup.

https://schema.org/TelevisionChannel
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class TelevisionChannelInheritedProperties(TypedDict):
    """A unique instance of a television BroadcastService on a CableOrSatelliteService lineup.

    References:
        https://schema.org/TelevisionChannel
    Note:
        Model Depth 4
    Attributes:
        broadcastChannelId: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The unique address by which the BroadcastService can be identified in a provider lineup. In US, this is typically a number.
        providesBroadcastService: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The BroadcastService offered on this channel.
        genre: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): Genre of the creative work, broadcast channel or group.
        broadcastServiceTier: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The type of service required to have access to the channel (e.g. Standard or Premium).
        inBroadcastLineup: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The CableOrSatelliteService offering the channel.
        broadcastFrequency: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The frequency used for over-the-air broadcasts. Numeric values or simple ranges, e.g. 87-99. In addition a shortcut idiom is supported for frequences of AM and FM radio channels, e.g. "87 FM".
    """

    broadcastChannelId: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    providesBroadcastService: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    genre: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    broadcastServiceTier: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    inBroadcastLineup: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    broadcastFrequency: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    


class TelevisionChannelProperties(TypedDict):
    """A unique instance of a television BroadcastService on a CableOrSatelliteService lineup.

    References:
        https://schema.org/TelevisionChannel
    Note:
        Model Depth 4
    Attributes:
    """

    

#TelevisionChannelInheritedPropertiesTd = TelevisionChannelInheritedProperties()
#TelevisionChannelPropertiesTd = TelevisionChannelProperties()


class AllProperties(TelevisionChannelInheritedProperties , TelevisionChannelProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[TelevisionChannelProperties, TelevisionChannelInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "TelevisionChannel"
    return model
    

TelevisionChannel = create_schema_org_model()