"""
For a [[VideoGame]], such as used with a [[PlayGameAction]], an enumeration of the kind of game availability offered. 

https://schema.org/GameAvailabilityEnumeration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class GameAvailabilityEnumerationInheritedProperties(TypedDict):
    """For a [[VideoGame]], such as used with a [[PlayGameAction]], an enumeration of the kind of game availability offered. 

    References:
        https://schema.org/GameAvailabilityEnumeration
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class GameAvailabilityEnumerationProperties(TypedDict):
    """For a [[VideoGame]], such as used with a [[PlayGameAction]], an enumeration of the kind of game availability offered. 

    References:
        https://schema.org/GameAvailabilityEnumeration
    Note:
        Model Depth 4
    Attributes:
    """

    

#GameAvailabilityEnumerationInheritedPropertiesTd = GameAvailabilityEnumerationInheritedProperties()
#GameAvailabilityEnumerationPropertiesTd = GameAvailabilityEnumerationProperties()


class AllProperties(GameAvailabilityEnumerationInheritedProperties , GameAvailabilityEnumerationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[GameAvailabilityEnumerationProperties, GameAvailabilityEnumerationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "GameAvailabilityEnumeration"
    return model
    

GameAvailabilityEnumeration = create_schema_org_model()