"""
The kind of release which this album is: single, EP or album.

https://schema.org/MusicAlbumReleaseType
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MusicAlbumReleaseTypeInheritedProperties(TypedDict):
    """The kind of release which this album is: single, EP or album.

    References:
        https://schema.org/MusicAlbumReleaseType
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class MusicAlbumReleaseTypeProperties(TypedDict):
    """The kind of release which this album is: single, EP or album.

    References:
        https://schema.org/MusicAlbumReleaseType
    Note:
        Model Depth 4
    Attributes:
    """

    

#MusicAlbumReleaseTypeInheritedPropertiesTd = MusicAlbumReleaseTypeInheritedProperties()
#MusicAlbumReleaseTypePropertiesTd = MusicAlbumReleaseTypeProperties()


class AllProperties(MusicAlbumReleaseTypeInheritedProperties , MusicAlbumReleaseTypeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MusicAlbumReleaseTypeProperties, MusicAlbumReleaseTypeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MusicAlbumReleaseType"
    return model
    

MusicAlbumReleaseType = create_schema_org_model()