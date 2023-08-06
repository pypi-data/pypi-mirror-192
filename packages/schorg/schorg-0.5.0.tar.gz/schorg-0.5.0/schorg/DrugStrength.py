"""
A specific strength in which a medical drug is available in a specific country.

https://schema.org/DrugStrength
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DrugStrengthInheritedProperties(TypedDict):
    """A specific strength in which a medical drug is available in a specific country.

    References:
        https://schema.org/DrugStrength
    Note:
        Model Depth 4
    Attributes:
    """

    


class DrugStrengthProperties(TypedDict):
    """A specific strength in which a medical drug is available in a specific country.

    References:
        https://schema.org/DrugStrength
    Note:
        Model Depth 4
    Attributes:
        activeIngredient: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): An active ingredient, typically chemical compounds and/or biologic substances.
        availableIn: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The location in which the strength is available.
        strengthValue: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The value of an active ingredient's strength, e.g. 325.
        strengthUnit: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The units of an active ingredient's strength, e.g. mg.
        maximumIntake: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Recommended intake of this supplement for a given population as defined by a specific recommending authority.
    """

    activeIngredient: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    availableIn: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    strengthValue: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    strengthUnit: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    maximumIntake: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#DrugStrengthInheritedPropertiesTd = DrugStrengthInheritedProperties()
#DrugStrengthPropertiesTd = DrugStrengthProperties()


class AllProperties(DrugStrengthInheritedProperties , DrugStrengthProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DrugStrengthProperties, DrugStrengthInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DrugStrength"
    return model
    

DrugStrength = create_schema_org_model()