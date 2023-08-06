"""
Stages that can be observed from a topic.

https://schema.org/StagesHealthAspect
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class StagesHealthAspectInheritedProperties(TypedDict):
    """Stages that can be observed from a topic.

    References:
        https://schema.org/StagesHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    


class StagesHealthAspectProperties(TypedDict):
    """Stages that can be observed from a topic.

    References:
        https://schema.org/StagesHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    

#StagesHealthAspectInheritedPropertiesTd = StagesHealthAspectInheritedProperties()
#StagesHealthAspectPropertiesTd = StagesHealthAspectProperties()


class AllProperties(StagesHealthAspectInheritedProperties , StagesHealthAspectProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[StagesHealthAspectProperties, StagesHealthAspectInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "StagesHealthAspect"
    return model
    

StagesHealthAspect = create_schema_org_model()