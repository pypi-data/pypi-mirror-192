"""
The act of asserting that a future event/action is no longer going to happen.Related actions:* [[ConfirmAction]]: The antonym of CancelAction.

https://schema.org/CancelAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CancelActionInheritedProperties(TypedDict):
    """The act of asserting that a future event/action is no longer going to happen.Related actions:* [[ConfirmAction]]: The antonym of CancelAction.

    References:
        https://schema.org/CancelAction
    Note:
        Model Depth 5
    Attributes:
        scheduledTime: (Optional[Union[List[Union[datetime, SchemaOrgObj, str]], datetime, SchemaOrgObj, str]]): The time the object is scheduled to.
    """

    scheduledTime: NotRequired[Union[List[Union[datetime, SchemaOrgObj, str]], datetime, SchemaOrgObj, str]]
    


class CancelActionProperties(TypedDict):
    """The act of asserting that a future event/action is no longer going to happen.Related actions:* [[ConfirmAction]]: The antonym of CancelAction.

    References:
        https://schema.org/CancelAction
    Note:
        Model Depth 5
    Attributes:
    """

    

#CancelActionInheritedPropertiesTd = CancelActionInheritedProperties()
#CancelActionPropertiesTd = CancelActionProperties()


class AllProperties(CancelActionInheritedProperties , CancelActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CancelActionProperties, CancelActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "CancelAction"
    return model
    

CancelAction = create_schema_org_model()