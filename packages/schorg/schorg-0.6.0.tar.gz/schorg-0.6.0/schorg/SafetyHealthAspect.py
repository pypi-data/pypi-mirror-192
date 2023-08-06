"""
Content about the safety-related aspects of a health topic.

https://schema.org/SafetyHealthAspect
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SafetyHealthAspectInheritedProperties(TypedDict):
    """Content about the safety-related aspects of a health topic.

    References:
        https://schema.org/SafetyHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    


class SafetyHealthAspectProperties(TypedDict):
    """Content about the safety-related aspects of a health topic.

    References:
        https://schema.org/SafetyHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    

#SafetyHealthAspectInheritedPropertiesTd = SafetyHealthAspectInheritedProperties()
#SafetyHealthAspectPropertiesTd = SafetyHealthAspectProperties()


class AllProperties(SafetyHealthAspectInheritedProperties , SafetyHealthAspectProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SafetyHealthAspectProperties, SafetyHealthAspectInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "SafetyHealthAspect"
    return model
    

SafetyHealthAspect = create_schema_org_model()