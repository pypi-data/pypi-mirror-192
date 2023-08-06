"""
A diet exclusive of animal meat.

https://schema.org/VegetarianDiet
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class VegetarianDietInheritedProperties(TypedDict):
    """A diet exclusive of animal meat.

    References:
        https://schema.org/VegetarianDiet
    Note:
        Model Depth 5
    Attributes:
    """

    


class VegetarianDietProperties(TypedDict):
    """A diet exclusive of animal meat.

    References:
        https://schema.org/VegetarianDiet
    Note:
        Model Depth 5
    Attributes:
    """

    

#VegetarianDietInheritedPropertiesTd = VegetarianDietInheritedProperties()
#VegetarianDietPropertiesTd = VegetarianDietProperties()


class AllProperties(VegetarianDietInheritedProperties , VegetarianDietProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[VegetarianDietProperties, VegetarianDietInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "VegetarianDiet"
    return model
    

VegetarianDiet = create_schema_org_model()