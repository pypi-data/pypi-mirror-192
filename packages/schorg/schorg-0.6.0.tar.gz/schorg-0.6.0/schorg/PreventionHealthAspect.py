"""
Information about actions or measures that can be taken to avoid getting the topic or reaching a critical situation related to the topic.

https://schema.org/PreventionHealthAspect
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PreventionHealthAspectInheritedProperties(TypedDict):
    """Information about actions or measures that can be taken to avoid getting the topic or reaching a critical situation related to the topic.

    References:
        https://schema.org/PreventionHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    


class PreventionHealthAspectProperties(TypedDict):
    """Information about actions or measures that can be taken to avoid getting the topic or reaching a critical situation related to the topic.

    References:
        https://schema.org/PreventionHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    

#PreventionHealthAspectInheritedPropertiesTd = PreventionHealthAspectInheritedProperties()
#PreventionHealthAspectPropertiesTd = PreventionHealthAspectProperties()


class AllProperties(PreventionHealthAspectInheritedProperties , PreventionHealthAspectProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PreventionHealthAspectProperties, PreventionHealthAspectInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PreventionHealthAspect"
    return model
    

PreventionHealthAspect = create_schema_org_model()