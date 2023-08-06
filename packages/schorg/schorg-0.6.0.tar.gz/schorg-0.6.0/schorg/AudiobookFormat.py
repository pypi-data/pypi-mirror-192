"""
Book format: Audiobook. This is an enumerated value for use with the bookFormat property. There is also a type 'Audiobook' in the bib extension which includes Audiobook specific properties.

https://schema.org/AudiobookFormat
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AudiobookFormatInheritedProperties(TypedDict):
    """Book format: Audiobook. This is an enumerated value for use with the bookFormat property. There is also a type 'Audiobook' in the bib extension which includes Audiobook specific properties.

    References:
        https://schema.org/AudiobookFormat
    Note:
        Model Depth 5
    Attributes:
    """

    


class AudiobookFormatProperties(TypedDict):
    """Book format: Audiobook. This is an enumerated value for use with the bookFormat property. There is also a type 'Audiobook' in the bib extension which includes Audiobook specific properties.

    References:
        https://schema.org/AudiobookFormat
    Note:
        Model Depth 5
    Attributes:
    """

    

#AudiobookFormatInheritedPropertiesTd = AudiobookFormatInheritedProperties()
#AudiobookFormatPropertiesTd = AudiobookFormatProperties()


class AllProperties(AudiobookFormatInheritedProperties , AudiobookFormatProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AudiobookFormatProperties, AudiobookFormatInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "AudiobookFormat"
    return model
    

AudiobookFormat = create_schema_org_model()