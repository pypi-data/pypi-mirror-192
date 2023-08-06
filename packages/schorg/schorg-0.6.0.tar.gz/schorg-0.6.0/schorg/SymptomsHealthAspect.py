"""
Symptoms or related symptoms of a Topic.

https://schema.org/SymptomsHealthAspect
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SymptomsHealthAspectInheritedProperties(TypedDict):
    """Symptoms or related symptoms of a Topic.

    References:
        https://schema.org/SymptomsHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    


class SymptomsHealthAspectProperties(TypedDict):
    """Symptoms or related symptoms of a Topic.

    References:
        https://schema.org/SymptomsHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    

#SymptomsHealthAspectInheritedPropertiesTd = SymptomsHealthAspectInheritedProperties()
#SymptomsHealthAspectPropertiesTd = SymptomsHealthAspectProperties()


class AllProperties(SymptomsHealthAspectInheritedProperties , SymptomsHealthAspectProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SymptomsHealthAspectProperties, SymptomsHealthAspectInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "SymptomsHealthAspect"
    return model
    

SymptomsHealthAspect = create_schema_org_model()