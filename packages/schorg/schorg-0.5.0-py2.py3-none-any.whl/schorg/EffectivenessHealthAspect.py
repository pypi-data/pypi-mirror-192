"""
Content about the effectiveness-related aspects of a health topic.

https://schema.org/EffectivenessHealthAspect
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EffectivenessHealthAspectInheritedProperties(TypedDict):
    """Content about the effectiveness-related aspects of a health topic.

    References:
        https://schema.org/EffectivenessHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    


class EffectivenessHealthAspectProperties(TypedDict):
    """Content about the effectiveness-related aspects of a health topic.

    References:
        https://schema.org/EffectivenessHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    

#EffectivenessHealthAspectInheritedPropertiesTd = EffectivenessHealthAspectInheritedProperties()
#EffectivenessHealthAspectPropertiesTd = EffectivenessHealthAspectProperties()


class AllProperties(EffectivenessHealthAspectInheritedProperties , EffectivenessHealthAspectProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EffectivenessHealthAspectProperties, EffectivenessHealthAspectInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "EffectivenessHealthAspect"
    return model
    

EffectivenessHealthAspect = create_schema_org_model()