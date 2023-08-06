"""
The act of arriving at a place. An agent arrives at a destination from a fromLocation, optionally with participants.

https://schema.org/ArriveAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ArriveActionInheritedProperties(TypedDict):
    """The act of arriving at a place. An agent arrives at a destination from a fromLocation, optionally with participants.

    References:
        https://schema.org/ArriveAction
    Note:
        Model Depth 4
    Attributes:
        toLocation: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of location. The final location of the object or the agent after the action.
        fromLocation: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of location. The original location of the object or the agent before the action.
    """

    toLocation: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    fromLocation: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class ArriveActionProperties(TypedDict):
    """The act of arriving at a place. An agent arrives at a destination from a fromLocation, optionally with participants.

    References:
        https://schema.org/ArriveAction
    Note:
        Model Depth 4
    Attributes:
    """

    

#ArriveActionInheritedPropertiesTd = ArriveActionInheritedProperties()
#ArriveActionPropertiesTd = ArriveActionProperties()


class AllProperties(ArriveActionInheritedProperties , ArriveActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ArriveActionProperties, ArriveActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ArriveAction"
    return model
    

ArriveAction = create_schema_org_model()