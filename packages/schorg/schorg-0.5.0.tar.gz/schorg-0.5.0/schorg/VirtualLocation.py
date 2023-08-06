"""
An online or virtual location for attending events. For example, one may attend an online seminar or educational event. While a virtual location may be used as the location of an event, virtual locations should not be confused with physical locations in the real world.

https://schema.org/VirtualLocation
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class VirtualLocationInheritedProperties(TypedDict):
    """An online or virtual location for attending events. For example, one may attend an online seminar or educational event. While a virtual location may be used as the location of an event, virtual locations should not be confused with physical locations in the real world.

    References:
        https://schema.org/VirtualLocation
    Note:
        Model Depth 3
    Attributes:
    """

    


class VirtualLocationProperties(TypedDict):
    """An online or virtual location for attending events. For example, one may attend an online seminar or educational event. While a virtual location may be used as the location of an event, virtual locations should not be confused with physical locations in the real world.

    References:
        https://schema.org/VirtualLocation
    Note:
        Model Depth 3
    Attributes:
    """

    

#VirtualLocationInheritedPropertiesTd = VirtualLocationInheritedProperties()
#VirtualLocationPropertiesTd = VirtualLocationProperties()


class AllProperties(VirtualLocationInheritedProperties , VirtualLocationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[VirtualLocationProperties, VirtualLocationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "VirtualLocation"
    return model
    

VirtualLocation = create_schema_org_model()