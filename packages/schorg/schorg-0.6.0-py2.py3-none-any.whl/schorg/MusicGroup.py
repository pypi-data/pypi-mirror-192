"""
A musical group, such as a band, an orchestra, or a choir. Can also be a solo musician.

https://schema.org/MusicGroup
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MusicGroupInheritedProperties(TypedDict):
    """A musical group, such as a band, an orchestra, or a choir. Can also be a solo musician.

    References:
        https://schema.org/MusicGroup
    Note:
        Model Depth 4
    Attributes:
    """

    


class MusicGroupProperties(TypedDict):
    """A musical group, such as a band, an orchestra, or a choir. Can also be a solo musician.

    References:
        https://schema.org/MusicGroup
    Note:
        Model Depth 4
    Attributes:
        album: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A music album.
        tracks: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A music recording (track)&#x2014;usually a single song.
        track: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A music recording (track)&#x2014;usually a single song. If an ItemList is given, the list should contain items of type MusicRecording.
        albums: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A collection of music albums.
        genre: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): Genre of the creative work, broadcast channel or group.
        musicGroupMember: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A member of a music group&#x2014;for example, John, Paul, George, or Ringo.
    """

    album: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    tracks: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    track: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    albums: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    genre: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    musicGroupMember: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#MusicGroupInheritedPropertiesTd = MusicGroupInheritedProperties()
#MusicGroupPropertiesTd = MusicGroupProperties()


class AllProperties(MusicGroupInheritedProperties , MusicGroupProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MusicGroupProperties, MusicGroupInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MusicGroup"
    return model
    

MusicGroup = create_schema_org_model()