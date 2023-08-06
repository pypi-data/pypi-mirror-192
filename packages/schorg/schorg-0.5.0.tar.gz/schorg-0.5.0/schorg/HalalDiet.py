"""
A diet conforming to Islamic dietary practices.

https://schema.org/HalalDiet
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class HalalDietInheritedProperties(TypedDict):
    """A diet conforming to Islamic dietary practices.

    References:
        https://schema.org/HalalDiet
    Note:
        Model Depth 5
    Attributes:
    """

    


class HalalDietProperties(TypedDict):
    """A diet conforming to Islamic dietary practices.

    References:
        https://schema.org/HalalDiet
    Note:
        Model Depth 5
    Attributes:
    """

    

#HalalDietInheritedPropertiesTd = HalalDietInheritedProperties()
#HalalDietPropertiesTd = HalalDietProperties()


class AllProperties(HalalDietInheritedProperties , HalalDietProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[HalalDietProperties, HalalDietInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "HalalDiet"
    return model
    

HalalDiet = create_schema_org_model()