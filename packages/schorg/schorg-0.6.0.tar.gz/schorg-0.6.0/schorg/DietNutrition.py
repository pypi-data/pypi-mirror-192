"""
Dietetics and nutrition as a medical specialty.

https://schema.org/DietNutrition
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DietNutritionInheritedProperties(TypedDict):
    """Dietetics and nutrition as a medical specialty.

    References:
        https://schema.org/DietNutrition
    Note:
        Model Depth 5
    Attributes:
    """

    


class DietNutritionProperties(TypedDict):
    """Dietetics and nutrition as a medical specialty.

    References:
        https://schema.org/DietNutrition
    Note:
        Model Depth 5
    Attributes:
    """

    

#DietNutritionInheritedPropertiesTd = DietNutritionInheritedProperties()
#DietNutritionPropertiesTd = DietNutritionProperties()


class AllProperties(DietNutritionInheritedProperties , DietNutritionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DietNutritionProperties, DietNutritionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DietNutrition"
    return model
    

DietNutrition = create_schema_org_model()