"""
Format of this release (the type of recording media used, i.e. compact disc, digital media, LP, etc.).

https://schema.org/MusicReleaseFormatType
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MusicReleaseFormatTypeInheritedProperties(TypedDict):
    """Format of this release (the type of recording media used, i.e. compact disc, digital media, LP, etc.).

    References:
        https://schema.org/MusicReleaseFormatType
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class MusicReleaseFormatTypeProperties(TypedDict):
    """Format of this release (the type of recording media used, i.e. compact disc, digital media, LP, etc.).

    References:
        https://schema.org/MusicReleaseFormatType
    Note:
        Model Depth 4
    Attributes:
    """

    

#MusicReleaseFormatTypeInheritedPropertiesTd = MusicReleaseFormatTypeInheritedProperties()
#MusicReleaseFormatTypePropertiesTd = MusicReleaseFormatTypeProperties()


class AllProperties(MusicReleaseFormatTypeInheritedProperties , MusicReleaseFormatTypeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MusicReleaseFormatTypeProperties, MusicReleaseFormatTypeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MusicReleaseFormatType"
    return model
    

MusicReleaseFormatType = create_schema_org_model()