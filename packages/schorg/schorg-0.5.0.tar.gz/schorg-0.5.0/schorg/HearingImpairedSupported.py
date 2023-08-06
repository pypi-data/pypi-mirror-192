"""
Uses devices to support users with hearing impairments.

https://schema.org/HearingImpairedSupported
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class HearingImpairedSupportedInheritedProperties(TypedDict):
    """Uses devices to support users with hearing impairments.

    References:
        https://schema.org/HearingImpairedSupported
    Note:
        Model Depth 5
    Attributes:
    """

    


class HearingImpairedSupportedProperties(TypedDict):
    """Uses devices to support users with hearing impairments.

    References:
        https://schema.org/HearingImpairedSupported
    Note:
        Model Depth 5
    Attributes:
    """

    

#HearingImpairedSupportedInheritedPropertiesTd = HearingImpairedSupportedInheritedProperties()
#HearingImpairedSupportedPropertiesTd = HearingImpairedSupportedProperties()


class AllProperties(HearingImpairedSupportedInheritedProperties , HearingImpairedSupportedProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[HearingImpairedSupportedProperties, HearingImpairedSupportedInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "HearingImpairedSupported"
    return model
    

HearingImpairedSupported = create_schema_org_model()