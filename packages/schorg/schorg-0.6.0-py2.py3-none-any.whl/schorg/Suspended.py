"""
Suspended.

https://schema.org/Suspended
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SuspendedInheritedProperties(TypedDict):
    """Suspended.

    References:
        https://schema.org/Suspended
    Note:
        Model Depth 6
    Attributes:
    """

    


class SuspendedProperties(TypedDict):
    """Suspended.

    References:
        https://schema.org/Suspended
    Note:
        Model Depth 6
    Attributes:
    """

    

#SuspendedInheritedPropertiesTd = SuspendedInheritedProperties()
#SuspendedPropertiesTd = SuspendedProperties()


class AllProperties(SuspendedInheritedProperties , SuspendedProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SuspendedProperties, SuspendedInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Suspended"
    return model
    

Suspended = create_schema_org_model()