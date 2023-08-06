"""
Information about the causes and main actions that gave rise to the topic.

https://schema.org/CausesHealthAspect
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CausesHealthAspectInheritedProperties(TypedDict):
    """Information about the causes and main actions that gave rise to the topic.

    References:
        https://schema.org/CausesHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    


class CausesHealthAspectProperties(TypedDict):
    """Information about the causes and main actions that gave rise to the topic.

    References:
        https://schema.org/CausesHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    

#CausesHealthAspectInheritedPropertiesTd = CausesHealthAspectInheritedProperties()
#CausesHealthAspectPropertiesTd = CausesHealthAspectProperties()


class AllProperties(CausesHealthAspectInheritedProperties , CausesHealthAspectProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CausesHealthAspectProperties, CausesHealthAspectInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "CausesHealthAspect"
    return model
    

CausesHealthAspect = create_schema_org_model()