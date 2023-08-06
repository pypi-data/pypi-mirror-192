"""
Content about the allergy-related aspects of a health topic.

https://schema.org/AllergiesHealthAspect
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AllergiesHealthAspectInheritedProperties(TypedDict):
    """Content about the allergy-related aspects of a health topic.

    References:
        https://schema.org/AllergiesHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    


class AllergiesHealthAspectProperties(TypedDict):
    """Content about the allergy-related aspects of a health topic.

    References:
        https://schema.org/AllergiesHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    

#AllergiesHealthAspectInheritedPropertiesTd = AllergiesHealthAspectInheritedProperties()
#AllergiesHealthAspectPropertiesTd = AllergiesHealthAspectProperties()


class AllProperties(AllergiesHealthAspectInheritedProperties , AllergiesHealthAspectProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AllergiesHealthAspectProperties, AllergiesHealthAspectInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "AllergiesHealthAspect"
    return model
    

AllergiesHealthAspect = create_schema_org_model()