"""
Classification of the album by its type of content: soundtrack, live album, studio album, etc.

https://schema.org/MusicAlbumProductionType
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MusicAlbumProductionTypeInheritedProperties(TypedDict):
    """Classification of the album by its type of content: soundtrack, live album, studio album, etc.

    References:
        https://schema.org/MusicAlbumProductionType
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class MusicAlbumProductionTypeProperties(TypedDict):
    """Classification of the album by its type of content: soundtrack, live album, studio album, etc.

    References:
        https://schema.org/MusicAlbumProductionType
    Note:
        Model Depth 4
    Attributes:
    """

    

#MusicAlbumProductionTypeInheritedPropertiesTd = MusicAlbumProductionTypeInheritedProperties()
#MusicAlbumProductionTypePropertiesTd = MusicAlbumProductionTypeProperties()


class AllProperties(MusicAlbumProductionTypeInheritedProperties , MusicAlbumProductionTypeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MusicAlbumProductionTypeProperties, MusicAlbumProductionTypeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MusicAlbumProductionType"
    return model
    

MusicAlbumProductionType = create_schema_org_model()