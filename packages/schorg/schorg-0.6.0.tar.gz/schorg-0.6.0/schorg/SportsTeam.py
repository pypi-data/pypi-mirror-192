"""
Organization: Sports team.

https://schema.org/SportsTeam
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SportsTeamInheritedProperties(TypedDict):
    """Organization: Sports team.

    References:
        https://schema.org/SportsTeam
    Note:
        Model Depth 4
    Attributes:
        sport: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): A type of sport (e.g. Baseball).
    """

    sport: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    


class SportsTeamProperties(TypedDict):
    """Organization: Sports team.

    References:
        https://schema.org/SportsTeam
    Note:
        Model Depth 4
    Attributes:
        athlete: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A person that acts as performing member of a sports team; a player as opposed to a coach.
        gender: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Gender of something, typically a [[Person]], but possibly also fictional characters, animals, etc. While https://schema.org/Male and https://schema.org/Female may be used, text strings are also acceptable for people who do not identify as a binary gender. The [[gender]] property can also be used in an extended sense to cover e.g. the gender of sports teams. As with the gender of individuals, we do not try to enumerate all possibilities. A mixed-gender [[SportsTeam]] can be indicated with a text value of "Mixed".
        coach: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A person that acts in a coaching role for a sports team.
    """

    athlete: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    gender: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    coach: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#SportsTeamInheritedPropertiesTd = SportsTeamInheritedProperties()
#SportsTeamPropertiesTd = SportsTeamProperties()


class AllProperties(SportsTeamInheritedProperties , SportsTeamProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SportsTeamProperties, SportsTeamInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "SportsTeam"
    return model
    

SportsTeam = create_schema_org_model()