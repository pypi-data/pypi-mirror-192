"""
The act of being defeated in a competitive activity.

https://schema.org/LoseAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class LoseActionInheritedProperties(TypedDict):
    """The act of being defeated in a competitive activity.

    References:
        https://schema.org/LoseAction
    Note:
        Model Depth 4
    Attributes:
    """

    


class LoseActionProperties(TypedDict):
    """The act of being defeated in a competitive activity.

    References:
        https://schema.org/LoseAction
    Note:
        Model Depth 4
    Attributes:
        winner: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of participant. The winner of the action.
    """

    winner: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#LoseActionInheritedPropertiesTd = LoseActionInheritedProperties()
#LoseActionPropertiesTd = LoseActionProperties()


class AllProperties(LoseActionInheritedProperties , LoseActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[LoseActionProperties, LoseActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "LoseAction"
    return model
    

LoseAction = create_schema_org_model()