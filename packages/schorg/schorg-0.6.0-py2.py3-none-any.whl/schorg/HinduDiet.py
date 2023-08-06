"""
A diet conforming to Hindu dietary practices, in particular, beef-free.

https://schema.org/HinduDiet
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class HinduDietInheritedProperties(TypedDict):
    """A diet conforming to Hindu dietary practices, in particular, beef-free.

    References:
        https://schema.org/HinduDiet
    Note:
        Model Depth 5
    Attributes:
    """

    


class HinduDietProperties(TypedDict):
    """A diet conforming to Hindu dietary practices, in particular, beef-free.

    References:
        https://schema.org/HinduDiet
    Note:
        Model Depth 5
    Attributes:
    """

    

#HinduDietInheritedPropertiesTd = HinduDietInheritedProperties()
#HinduDietPropertiesTd = HinduDietProperties()


class AllProperties(HinduDietInheritedProperties , HinduDietProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[HinduDietProperties, HinduDietInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "HinduDiet"
    return model
    

HinduDiet = create_schema_org_model()