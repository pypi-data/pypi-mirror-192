"""
Information about the risk factors and possible complications that may follow a topic.

https://schema.org/RisksOrComplicationsHealthAspect
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class RisksOrComplicationsHealthAspectInheritedProperties(TypedDict):
    """Information about the risk factors and possible complications that may follow a topic.

    References:
        https://schema.org/RisksOrComplicationsHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    


class RisksOrComplicationsHealthAspectProperties(TypedDict):
    """Information about the risk factors and possible complications that may follow a topic.

    References:
        https://schema.org/RisksOrComplicationsHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    

#RisksOrComplicationsHealthAspectInheritedPropertiesTd = RisksOrComplicationsHealthAspectInheritedProperties()
#RisksOrComplicationsHealthAspectPropertiesTd = RisksOrComplicationsHealthAspectProperties()


class AllProperties(RisksOrComplicationsHealthAspectInheritedProperties , RisksOrComplicationsHealthAspectProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[RisksOrComplicationsHealthAspectProperties, RisksOrComplicationsHealthAspectInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "RisksOrComplicationsHealthAspect"
    return model
    

RisksOrComplicationsHealthAspect = create_schema_org_model()