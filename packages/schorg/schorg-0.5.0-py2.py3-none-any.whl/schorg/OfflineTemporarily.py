"""
Game server status: OfflineTemporarily. Server is offline now but it can be online soon.

https://schema.org/OfflineTemporarily
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OfflineTemporarilyInheritedProperties(TypedDict):
    """Game server status: OfflineTemporarily. Server is offline now but it can be online soon.

    References:
        https://schema.org/OfflineTemporarily
    Note:
        Model Depth 6
    Attributes:
    """

    


class OfflineTemporarilyProperties(TypedDict):
    """Game server status: OfflineTemporarily. Server is offline now but it can be online soon.

    References:
        https://schema.org/OfflineTemporarily
    Note:
        Model Depth 6
    Attributes:
    """

    

#OfflineTemporarilyInheritedPropertiesTd = OfflineTemporarilyInheritedProperties()
#OfflineTemporarilyPropertiesTd = OfflineTemporarilyProperties()


class AllProperties(OfflineTemporarilyInheritedProperties , OfflineTemporarilyProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OfflineTemporarilyProperties, OfflineTemporarilyInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OfflineTemporarily"
    return model
    

OfflineTemporarily = create_schema_org_model()