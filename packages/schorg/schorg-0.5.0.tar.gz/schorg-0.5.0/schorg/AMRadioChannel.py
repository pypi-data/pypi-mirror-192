"""
A radio channel that uses AM.

https://schema.org/AMRadioChannel
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AMRadioChannelInheritedProperties(TypedDict):
    """A radio channel that uses AM.

    References:
        https://schema.org/AMRadioChannel
    Note:
        Model Depth 5
    Attributes:
    """

    


class AMRadioChannelProperties(TypedDict):
    """A radio channel that uses AM.

    References:
        https://schema.org/AMRadioChannel
    Note:
        Model Depth 5
    Attributes:
    """

    

#AMRadioChannelInheritedPropertiesTd = AMRadioChannelInheritedProperties()
#AMRadioChannelPropertiesTd = AMRadioChannelProperties()


class AllProperties(AMRadioChannelInheritedProperties , AMRadioChannelProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AMRadioChannelProperties, AMRadioChannelInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "AMRadioChannel"
    return model
    

AMRadioChannel = create_schema_org_model()