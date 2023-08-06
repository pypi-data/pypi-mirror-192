"""
A comedy club.

https://schema.org/ComedyClub
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ComedyClubInheritedProperties(TypedDict):
    """A comedy club.

    References:
        https://schema.org/ComedyClub
    Note:
        Model Depth 5
    Attributes:
    """

    


class ComedyClubProperties(TypedDict):
    """A comedy club.

    References:
        https://schema.org/ComedyClub
    Note:
        Model Depth 5
    Attributes:
    """

    

#ComedyClubInheritedPropertiesTd = ComedyClubInheritedProperties()
#ComedyClubPropertiesTd = ComedyClubProperties()


class AllProperties(ComedyClubInheritedProperties , ComedyClubProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ComedyClubProperties, ComedyClubInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ComedyClub"
    return model
    

ComedyClub = create_schema_org_model()