"""
Content about how to screen or further filter a topic.

https://schema.org/ScreeningHealthAspect
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ScreeningHealthAspectInheritedProperties(TypedDict):
    """Content about how to screen or further filter a topic.

    References:
        https://schema.org/ScreeningHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    


class ScreeningHealthAspectProperties(TypedDict):
    """Content about how to screen or further filter a topic.

    References:
        https://schema.org/ScreeningHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    

#ScreeningHealthAspectInheritedPropertiesTd = ScreeningHealthAspectInheritedProperties()
#ScreeningHealthAspectPropertiesTd = ScreeningHealthAspectProperties()


class AllProperties(ScreeningHealthAspectInheritedProperties , ScreeningHealthAspectProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ScreeningHealthAspectProperties, ScreeningHealthAspectInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ScreeningHealthAspect"
    return model
    

ScreeningHealthAspect = create_schema_org_model()