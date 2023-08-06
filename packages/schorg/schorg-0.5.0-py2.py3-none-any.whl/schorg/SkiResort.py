"""
A ski resort.

https://schema.org/SkiResort
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SkiResortInheritedProperties(TypedDict):
    """A ski resort.

    References:
        https://schema.org/SkiResort
    Note:
        Model Depth 5
    Attributes:
    """

    


class SkiResortProperties(TypedDict):
    """A ski resort.

    References:
        https://schema.org/SkiResort
    Note:
        Model Depth 5
    Attributes:
    """

    

#SkiResortInheritedPropertiesTd = SkiResortInheritedProperties()
#SkiResortPropertiesTd = SkiResortProperties()


class AllProperties(SkiResortInheritedProperties , SkiResortProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SkiResortProperties, SkiResortInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "SkiResort"
    return model
    

SkiResort = create_schema_org_model()