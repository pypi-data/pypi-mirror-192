"""
A reservoir of water, typically an artificially created lake, like the Lake Kariba reservoir.

https://schema.org/Reservoir
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ReservoirInheritedProperties(TypedDict):
    """A reservoir of water, typically an artificially created lake, like the Lake Kariba reservoir.

    References:
        https://schema.org/Reservoir
    Note:
        Model Depth 5
    Attributes:
    """

    


class ReservoirProperties(TypedDict):
    """A reservoir of water, typically an artificially created lake, like the Lake Kariba reservoir.

    References:
        https://schema.org/Reservoir
    Note:
        Model Depth 5
    Attributes:
    """

    

#ReservoirInheritedPropertiesTd = ReservoirInheritedProperties()
#ReservoirPropertiesTd = ReservoirProperties()


class AllProperties(ReservoirInheritedProperties , ReservoirProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ReservoirProperties, ReservoirInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Reservoir"
    return model
    

Reservoir = create_schema_org_model()