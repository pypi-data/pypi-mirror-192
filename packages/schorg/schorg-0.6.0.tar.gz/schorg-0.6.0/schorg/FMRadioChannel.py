"""
A radio channel that uses FM.

https://schema.org/FMRadioChannel
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class FMRadioChannelInheritedProperties(TypedDict):
    """A radio channel that uses FM.

    References:
        https://schema.org/FMRadioChannel
    Note:
        Model Depth 5
    Attributes:
    """

    


class FMRadioChannelProperties(TypedDict):
    """A radio channel that uses FM.

    References:
        https://schema.org/FMRadioChannel
    Note:
        Model Depth 5
    Attributes:
    """

    

#FMRadioChannelInheritedPropertiesTd = FMRadioChannelInheritedProperties()
#FMRadioChannelPropertiesTd = FMRadioChannelProperties()


class AllProperties(FMRadioChannelInheritedProperties , FMRadioChannelProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[FMRadioChannelProperties, FMRadioChannelInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "FMRadioChannel"
    return model
    

FMRadioChannel = create_schema_org_model()