"""
A diet focused on reduced calorie intake.

https://schema.org/LowCalorieDiet
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class LowCalorieDietInheritedProperties(TypedDict):
    """A diet focused on reduced calorie intake.

    References:
        https://schema.org/LowCalorieDiet
    Note:
        Model Depth 5
    Attributes:
    """

    


class LowCalorieDietProperties(TypedDict):
    """A diet focused on reduced calorie intake.

    References:
        https://schema.org/LowCalorieDiet
    Note:
        Model Depth 5
    Attributes:
    """

    

#LowCalorieDietInheritedPropertiesTd = LowCalorieDietInheritedProperties()
#LowCalorieDietPropertiesTd = LowCalorieDietProperties()


class AllProperties(LowCalorieDietInheritedProperties , LowCalorieDietProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[LowCalorieDietProperties, LowCalorieDietInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "LowCalorieDiet"
    return model
    

LowCalorieDiet = create_schema_org_model()