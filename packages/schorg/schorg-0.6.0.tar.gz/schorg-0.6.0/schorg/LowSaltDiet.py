"""
A diet focused on reduced sodium intake.

https://schema.org/LowSaltDiet
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class LowSaltDietInheritedProperties(TypedDict):
    """A diet focused on reduced sodium intake.

    References:
        https://schema.org/LowSaltDiet
    Note:
        Model Depth 5
    Attributes:
    """

    


class LowSaltDietProperties(TypedDict):
    """A diet focused on reduced sodium intake.

    References:
        https://schema.org/LowSaltDiet
    Note:
        Model Depth 5
    Attributes:
    """

    

#LowSaltDietInheritedPropertiesTd = LowSaltDietInheritedProperties()
#LowSaltDietPropertiesTd = LowSaltDietProperties()


class AllProperties(LowSaltDietInheritedProperties , LowSaltDietProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[LowSaltDietProperties, LowSaltDietInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "LowSaltDiet"
    return model
    

LowSaltDiet = create_schema_org_model()