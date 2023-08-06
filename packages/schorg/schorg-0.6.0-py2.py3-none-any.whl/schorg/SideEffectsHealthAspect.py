"""
Side effects that can be observed from the usage of the topic.

https://schema.org/SideEffectsHealthAspect
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SideEffectsHealthAspectInheritedProperties(TypedDict):
    """Side effects that can be observed from the usage of the topic.

    References:
        https://schema.org/SideEffectsHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    


class SideEffectsHealthAspectProperties(TypedDict):
    """Side effects that can be observed from the usage of the topic.

    References:
        https://schema.org/SideEffectsHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    

#SideEffectsHealthAspectInheritedPropertiesTd = SideEffectsHealthAspectInheritedProperties()
#SideEffectsHealthAspectPropertiesTd = SideEffectsHealthAspectProperties()


class AllProperties(SideEffectsHealthAspectInheritedProperties , SideEffectsHealthAspectProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SideEffectsHealthAspectProperties, SideEffectsHealthAspectInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "SideEffectsHealthAspect"
    return model
    

SideEffectsHealthAspect = create_schema_org_model()