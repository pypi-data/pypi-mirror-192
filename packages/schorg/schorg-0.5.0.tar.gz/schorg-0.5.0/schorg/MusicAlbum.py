"""
A collection of music tracks.

https://schema.org/MusicAlbum
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MusicAlbumInheritedProperties(TypedDict):
    """A collection of music tracks.

    References:
        https://schema.org/MusicAlbum
    Note:
        Model Depth 4
    Attributes:
        tracks: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A music recording (track)&#x2014;usually a single song.
        track: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A music recording (track)&#x2014;usually a single song. If an ItemList is given, the list should contain items of type MusicRecording.
        numTracks: (Optional[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]): The number of tracks in this album or playlist.
    """

    tracks: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    track: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    numTracks: NotRequired[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]
    


class MusicAlbumProperties(TypedDict):
    """A collection of music tracks.

    References:
        https://schema.org/MusicAlbum
    Note:
        Model Depth 4
    Attributes:
        albumReleaseType: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The kind of release which this album is: single, EP or album.
        albumRelease: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A release of this album.
        byArtist: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The artist that performed this album or recording.
        albumProductionType: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Classification of the album by its type of content: soundtrack, live album, studio album, etc.
    """

    albumReleaseType: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    albumRelease: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    byArtist: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    albumProductionType: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#MusicAlbumInheritedPropertiesTd = MusicAlbumInheritedProperties()
#MusicAlbumPropertiesTd = MusicAlbumProperties()


class AllProperties(MusicAlbumInheritedProperties , MusicAlbumProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MusicAlbumProperties, MusicAlbumInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MusicAlbum"
    return model
    

MusicAlbum = create_schema_org_model()