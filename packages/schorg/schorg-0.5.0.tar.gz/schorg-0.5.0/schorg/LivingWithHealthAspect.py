"""
Information about coping or life related to the topic.

https://schema.org/LivingWithHealthAspect
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class LivingWithHealthAspectInheritedProperties(TypedDict):
    """Information about coping or life related to the topic.

    References:
        https://schema.org/LivingWithHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    


class LivingWithHealthAspectProperties(TypedDict):
    """Information about coping or life related to the topic.

    References:
        https://schema.org/LivingWithHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    

#LivingWithHealthAspectInheritedPropertiesTd = LivingWithHealthAspectInheritedProperties()
#LivingWithHealthAspectPropertiesTd = LivingWithHealthAspectProperties()


class AllProperties(LivingWithHealthAspectInheritedProperties , LivingWithHealthAspectProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[LivingWithHealthAspectProperties, LivingWithHealthAspectInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "LivingWithHealthAspect"
    return model
    

LivingWithHealthAspect = create_schema_org_model()