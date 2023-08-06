"""
A hair salon.

https://schema.org/HairSalon
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class HairSalonInheritedProperties(TypedDict):
    """A hair salon.

    References:
        https://schema.org/HairSalon
    Note:
        Model Depth 5
    Attributes:
    """

    


class HairSalonProperties(TypedDict):
    """A hair salon.

    References:
        https://schema.org/HairSalon
    Note:
        Model Depth 5
    Attributes:
    """

    

#HairSalonInheritedPropertiesTd = HairSalonInheritedProperties()
#HairSalonPropertiesTd = HairSalonProperties()


class AllProperties(HairSalonInheritedProperties , HairSalonProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[HairSalonProperties, HairSalonInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "HairSalon"
    return model
    

HairSalon = create_schema_org_model()