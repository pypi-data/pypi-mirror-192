"""
The act of  departing from a place. An agent departs from a fromLocation for a destination, optionally with participants.

https://schema.org/DepartAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DepartActionInheritedProperties(TypedDict):
    """The act of  departing from a place. An agent departs from a fromLocation for a destination, optionally with participants.

    References:
        https://schema.org/DepartAction
    Note:
        Model Depth 4
    Attributes:
        toLocation: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of location. The final location of the object or the agent after the action.
        fromLocation: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of location. The original location of the object or the agent before the action.
    """

    toLocation: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    fromLocation: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class DepartActionProperties(TypedDict):
    """The act of  departing from a place. An agent departs from a fromLocation for a destination, optionally with participants.

    References:
        https://schema.org/DepartAction
    Note:
        Model Depth 4
    Attributes:
    """

    

#DepartActionInheritedPropertiesTd = DepartActionInheritedProperties()
#DepartActionPropertiesTd = DepartActionProperties()


class AllProperties(DepartActionInheritedProperties , DepartActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DepartActionProperties, DepartActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DepartAction"
    return model
    

DepartAction = create_schema_org_model()