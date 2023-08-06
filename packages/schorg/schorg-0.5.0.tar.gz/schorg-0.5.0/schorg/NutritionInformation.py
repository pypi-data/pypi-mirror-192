"""
Nutritional information about the recipe.

https://schema.org/NutritionInformation
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class NutritionInformationInheritedProperties(TypedDict):
    """Nutritional information about the recipe.

    References:
        https://schema.org/NutritionInformation
    Note:
        Model Depth 4
    Attributes:
    """

    


class NutritionInformationProperties(TypedDict):
    """Nutritional information about the recipe.

    References:
        https://schema.org/NutritionInformation
    Note:
        Model Depth 4
    Attributes:
        sodiumContent: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The number of milligrams of sodium.
        carbohydrateContent: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The number of grams of carbohydrates.
        fatContent: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The number of grams of fat.
        cholesterolContent: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The number of milligrams of cholesterol.
        calories: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The number of calories.
        unsaturatedFatContent: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The number of grams of unsaturated fat.
        sugarContent: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The number of grams of sugar.
        transFatContent: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The number of grams of trans fat.
        proteinContent: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The number of grams of protein.
        saturatedFatContent: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The number of grams of saturated fat.
        servingSize: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The serving size, in terms of the number of volume or mass.
        fiberContent: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The number of grams of fiber.
    """

    sodiumContent: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    carbohydrateContent: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    fatContent: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    cholesterolContent: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    calories: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    unsaturatedFatContent: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    sugarContent: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    transFatContent: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    proteinContent: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    saturatedFatContent: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    servingSize: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    fiberContent: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#NutritionInformationInheritedPropertiesTd = NutritionInformationInheritedProperties()
#NutritionInformationPropertiesTd = NutritionInformationProperties()


class AllProperties(NutritionInformationInheritedProperties , NutritionInformationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[NutritionInformationProperties, NutritionInformationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "NutritionInformation"
    return model
    

NutritionInformation = create_schema_org_model()