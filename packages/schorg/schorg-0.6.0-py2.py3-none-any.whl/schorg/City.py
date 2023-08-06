"""
A city or town.

https://schema.org/City
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CityInheritedProperties(TypedDict):
    """A city or town.

    References:
        https://schema.org/City
    Note:
        Model Depth 4
    Attributes:
    """

    


class CityProperties(TypedDict):
    """A city or town.

    References:
        https://schema.org/City
    Note:
        Model Depth 4
    Attributes:
    """

    

#CityInheritedPropertiesTd = CityInheritedProperties()
#CityPropertiesTd = CityProperties()


class AllProperties(CityInheritedProperties , CityProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CityProperties, CityInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "City"
    return model
    

City = create_schema_org_model()