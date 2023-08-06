"""
A pond.

https://schema.org/Pond
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PondInheritedProperties(TypedDict):
    """A pond.

    References:
        https://schema.org/Pond
    Note:
        Model Depth 5
    Attributes:
    """

    


class PondProperties(TypedDict):
    """A pond.

    References:
        https://schema.org/Pond
    Note:
        Model Depth 5
    Attributes:
    """

    

#PondInheritedPropertiesTd = PondInheritedProperties()
#PondPropertiesTd = PondProperties()


class AllProperties(PondInheritedProperties , PondProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PondProperties, PondInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Pond"
    return model
    

Pond = create_schema_org_model()