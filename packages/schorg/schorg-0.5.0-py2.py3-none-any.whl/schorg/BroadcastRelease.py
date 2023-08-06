"""
BroadcastRelease.

https://schema.org/BroadcastRelease
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BroadcastReleaseInheritedProperties(TypedDict):
    """BroadcastRelease.

    References:
        https://schema.org/BroadcastRelease
    Note:
        Model Depth 5
    Attributes:
    """

    


class BroadcastReleaseProperties(TypedDict):
    """BroadcastRelease.

    References:
        https://schema.org/BroadcastRelease
    Note:
        Model Depth 5
    Attributes:
    """

    

#BroadcastReleaseInheritedPropertiesTd = BroadcastReleaseInheritedProperties()
#BroadcastReleasePropertiesTd = BroadcastReleaseProperties()


class AllProperties(BroadcastReleaseInheritedProperties , BroadcastReleaseProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BroadcastReleaseProperties, BroadcastReleaseInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BroadcastRelease"
    return model
    

BroadcastRelease = create_schema_org_model()