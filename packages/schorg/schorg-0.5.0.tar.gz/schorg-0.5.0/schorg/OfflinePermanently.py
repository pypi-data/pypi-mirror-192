"""
Game server status: OfflinePermanently. Server is offline and not available.

https://schema.org/OfflinePermanently
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OfflinePermanentlyInheritedProperties(TypedDict):
    """Game server status: OfflinePermanently. Server is offline and not available.

    References:
        https://schema.org/OfflinePermanently
    Note:
        Model Depth 6
    Attributes:
    """

    


class OfflinePermanentlyProperties(TypedDict):
    """Game server status: OfflinePermanently. Server is offline and not available.

    References:
        https://schema.org/OfflinePermanently
    Note:
        Model Depth 6
    Attributes:
    """

    

#OfflinePermanentlyInheritedPropertiesTd = OfflinePermanentlyInheritedProperties()
#OfflinePermanentlyPropertiesTd = OfflinePermanentlyProperties()


class AllProperties(OfflinePermanentlyInheritedProperties , OfflinePermanentlyProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OfflinePermanentlyProperties, OfflinePermanentlyInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OfflinePermanently"
    return model
    

OfflinePermanently = create_schema_org_model()