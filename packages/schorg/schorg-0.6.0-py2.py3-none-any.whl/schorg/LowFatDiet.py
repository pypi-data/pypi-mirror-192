"""
A diet focused on reduced fat and cholesterol intake.

https://schema.org/LowFatDiet
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class LowFatDietInheritedProperties(TypedDict):
    """A diet focused on reduced fat and cholesterol intake.

    References:
        https://schema.org/LowFatDiet
    Note:
        Model Depth 5
    Attributes:
    """

    


class LowFatDietProperties(TypedDict):
    """A diet focused on reduced fat and cholesterol intake.

    References:
        https://schema.org/LowFatDiet
    Note:
        Model Depth 5
    Attributes:
    """

    

#LowFatDietInheritedPropertiesTd = LowFatDietInheritedProperties()
#LowFatDietPropertiesTd = LowFatDietProperties()


class AllProperties(LowFatDietInheritedProperties , LowFatDietProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[LowFatDietProperties, LowFatDietInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "LowFatDiet"
    return model
    

LowFatDiet = create_schema_org_model()