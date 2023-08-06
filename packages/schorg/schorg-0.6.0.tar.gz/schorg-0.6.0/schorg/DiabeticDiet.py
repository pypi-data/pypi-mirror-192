"""
A diet appropriate for people with diabetes.

https://schema.org/DiabeticDiet
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DiabeticDietInheritedProperties(TypedDict):
    """A diet appropriate for people with diabetes.

    References:
        https://schema.org/DiabeticDiet
    Note:
        Model Depth 5
    Attributes:
    """

    


class DiabeticDietProperties(TypedDict):
    """A diet appropriate for people with diabetes.

    References:
        https://schema.org/DiabeticDiet
    Note:
        Model Depth 5
    Attributes:
    """

    

#DiabeticDietInheritedPropertiesTd = DiabeticDietInheritedProperties()
#DiabeticDietPropertiesTd = DiabeticDietProperties()


class AllProperties(DiabeticDietInheritedProperties , DiabeticDietProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DiabeticDietProperties, DiabeticDietInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DiabeticDiet"
    return model
    

DiabeticDiet = create_schema_org_model()