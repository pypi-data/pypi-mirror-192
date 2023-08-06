"""
The status of an Action.

https://schema.org/ActionStatusType
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ActionStatusTypeInheritedProperties(TypedDict):
    """The status of an Action.

    References:
        https://schema.org/ActionStatusType
    Note:
        Model Depth 5
    Attributes:
    """

    


class ActionStatusTypeProperties(TypedDict):
    """The status of an Action.

    References:
        https://schema.org/ActionStatusType
    Note:
        Model Depth 5
    Attributes:
    """

    

#ActionStatusTypeInheritedPropertiesTd = ActionStatusTypeInheritedProperties()
#ActionStatusTypePropertiesTd = ActionStatusTypeProperties()


class AllProperties(ActionStatusTypeInheritedProperties , ActionStatusTypeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ActionStatusTypeProperties, ActionStatusTypeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ActionStatusType"
    return model
    

ActionStatusType = create_schema_org_model()