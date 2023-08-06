"""
One of the continents (for example, Europe or Africa).

https://schema.org/Continent
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ContinentInheritedProperties(TypedDict):
    """One of the continents (for example, Europe or Africa).

    References:
        https://schema.org/Continent
    Note:
        Model Depth 4
    Attributes:
    """

    


class ContinentProperties(TypedDict):
    """One of the continents (for example, Europe or Africa).

    References:
        https://schema.org/Continent
    Note:
        Model Depth 4
    Attributes:
    """

    

#ContinentInheritedPropertiesTd = ContinentInheritedProperties()
#ContinentPropertiesTd = ContinentProperties()


class AllProperties(ContinentInheritedProperties , ContinentProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ContinentProperties, ContinentInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Continent"
    return model
    

Continent = create_schema_org_model()