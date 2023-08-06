"""
A health club.

https://schema.org/HealthClub
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class HealthClubInheritedProperties(TypedDict):
    """A health club.

    References:
        https://schema.org/HealthClub
    Note:
        Model Depth 5
    Attributes:
    """

    


class HealthClubProperties(TypedDict):
    """A health club.

    References:
        https://schema.org/HealthClub
    Note:
        Model Depth 5
    Attributes:
    """

    

#HealthClubInheritedPropertiesTd = HealthClubInheritedProperties()
#HealthClubPropertiesTd = HealthClubProperties()


class AllProperties(HealthClubInheritedProperties , HealthClubProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[HealthClubProperties, HealthClubInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "HealthClub"
    return model
    

HealthClub = create_schema_org_model()