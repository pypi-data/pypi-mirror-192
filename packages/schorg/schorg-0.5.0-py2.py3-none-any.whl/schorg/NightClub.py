"""
A nightclub or discotheque.

https://schema.org/NightClub
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class NightClubInheritedProperties(TypedDict):
    """A nightclub or discotheque.

    References:
        https://schema.org/NightClub
    Note:
        Model Depth 5
    Attributes:
    """

    


class NightClubProperties(TypedDict):
    """A nightclub or discotheque.

    References:
        https://schema.org/NightClub
    Note:
        Model Depth 5
    Attributes:
    """

    

#NightClubInheritedPropertiesTd = NightClubInheritedProperties()
#NightClubPropertiesTd = NightClubProperties()


class AllProperties(NightClubInheritedProperties , NightClubProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[NightClubProperties, NightClubInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "NightClub"
    return model
    

NightClub = create_schema_org_model()