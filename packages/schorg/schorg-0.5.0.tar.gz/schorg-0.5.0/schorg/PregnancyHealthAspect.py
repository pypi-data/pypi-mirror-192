"""
Content discussing pregnancy-related aspects of a health topic.

https://schema.org/PregnancyHealthAspect
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PregnancyHealthAspectInheritedProperties(TypedDict):
    """Content discussing pregnancy-related aspects of a health topic.

    References:
        https://schema.org/PregnancyHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    


class PregnancyHealthAspectProperties(TypedDict):
    """Content discussing pregnancy-related aspects of a health topic.

    References:
        https://schema.org/PregnancyHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    

#PregnancyHealthAspectInheritedPropertiesTd = PregnancyHealthAspectInheritedProperties()
#PregnancyHealthAspectPropertiesTd = PregnancyHealthAspectProperties()


class AllProperties(PregnancyHealthAspectInheritedProperties , PregnancyHealthAspectProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PregnancyHealthAspectProperties, PregnancyHealthAspectInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PregnancyHealthAspect"
    return model
    

PregnancyHealthAspect = create_schema_org_model()