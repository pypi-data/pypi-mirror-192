"""
A MusicRelease is a specific release of a music album.

https://schema.org/MusicRelease
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MusicReleaseInheritedProperties(TypedDict):
    """A MusicRelease is a specific release of a music album.

    References:
        https://schema.org/MusicRelease
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
    


class MusicReleaseProperties(TypedDict):
    """A MusicRelease is a specific release of a music album.

    References:
        https://schema.org/MusicRelease
    Note:
        Model Depth 4
    Attributes:
        releaseOf: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The album this is a release of.
        musicReleaseFormat: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Format of this release (the type of recording media used, i.e. compact disc, digital media, LP, etc.).
        duration: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The duration of the item (movie, audio recording, event, etc.) in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601).
        recordLabel: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The label that issued the release.
        catalogNumber: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The catalog number for the release.
        creditedTo: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The group the release is credited to if different than the byArtist. For example, Red and Blue is credited to "Stefani Germanotta Band", but by Lady Gaga.
    """

    releaseOf: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    musicReleaseFormat: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    duration: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    recordLabel: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    catalogNumber: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    creditedTo: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#MusicReleaseInheritedPropertiesTd = MusicReleaseInheritedProperties()
#MusicReleasePropertiesTd = MusicReleaseProperties()


class AllProperties(MusicReleaseInheritedProperties , MusicReleaseProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MusicReleaseProperties, MusicReleaseInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MusicRelease"
    return model
    

MusicRelease = create_schema_org_model()