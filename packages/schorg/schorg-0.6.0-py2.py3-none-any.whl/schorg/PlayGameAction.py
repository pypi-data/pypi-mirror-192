"""
The act of playing a video game.

https://schema.org/PlayGameAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PlayGameActionInheritedProperties(TypedDict):
    """The act of playing a video game.

    References:
        https://schema.org/PlayGameAction
    Note:
        Model Depth 4
    Attributes:
        actionAccessibilityRequirement: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A set of requirements that must be fulfilled in order to perform an Action. If more than one value is specified, fulfilling one set of requirements will allow the Action to be performed.
        expectsAcceptanceOf: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): An Offer which must be accepted before the user can perform the Action. For example, the user may need to buy a movie before being able to watch it.
    """

    actionAccessibilityRequirement: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    expectsAcceptanceOf: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class PlayGameActionProperties(TypedDict):
    """The act of playing a video game.

    References:
        https://schema.org/PlayGameAction
    Note:
        Model Depth 4
    Attributes:
        gameAvailabilityType: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Indicates the availability type of the game content associated with this action, such as whether it is a full version or a demo.
    """

    gameAvailabilityType: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    

#PlayGameActionInheritedPropertiesTd = PlayGameActionInheritedProperties()
#PlayGameActionPropertiesTd = PlayGameActionProperties()


class AllProperties(PlayGameActionInheritedProperties , PlayGameActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PlayGameActionProperties, PlayGameActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PlayGameAction"
    return model
    

PlayGameAction = create_schema_org_model()