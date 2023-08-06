"""
The act of achieving victory in a competitive activity.

https://schema.org/WinAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WinActionInheritedProperties(TypedDict):
    """The act of achieving victory in a competitive activity.

    References:
        https://schema.org/WinAction
    Note:
        Model Depth 4
    Attributes:
    """

    


class WinActionProperties(TypedDict):
    """The act of achieving victory in a competitive activity.

    References:
        https://schema.org/WinAction
    Note:
        Model Depth 4
    Attributes:
        loser: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of participant. The loser of the action.
    """

    loser: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#WinActionInheritedPropertiesTd = WinActionInheritedProperties()
#WinActionPropertiesTd = WinActionProperties()


class AllProperties(WinActionInheritedProperties , WinActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WinActionProperties, WinActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WinAction"
    return model
    

WinAction = create_schema_org_model()