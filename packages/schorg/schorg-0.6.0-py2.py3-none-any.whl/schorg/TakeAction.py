"""
The act of gaining ownership of an object from an origin. Reciprocal of GiveAction.Related actions:* [[GiveAction]]: The reciprocal of TakeAction.* [[ReceiveAction]]: Unlike ReceiveAction, TakeAction implies that ownership has been transferred.

https://schema.org/TakeAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class TakeActionInheritedProperties(TypedDict):
    """The act of gaining ownership of an object from an origin. Reciprocal of GiveAction.Related actions:* [[GiveAction]]: The reciprocal of TakeAction.* [[ReceiveAction]]: Unlike ReceiveAction, TakeAction implies that ownership has been transferred.

    References:
        https://schema.org/TakeAction
    Note:
        Model Depth 4
    Attributes:
        toLocation: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of location. The final location of the object or the agent after the action.
        fromLocation: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of location. The original location of the object or the agent before the action.
    """

    toLocation: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    fromLocation: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class TakeActionProperties(TypedDict):
    """The act of gaining ownership of an object from an origin. Reciprocal of GiveAction.Related actions:* [[GiveAction]]: The reciprocal of TakeAction.* [[ReceiveAction]]: Unlike ReceiveAction, TakeAction implies that ownership has been transferred.

    References:
        https://schema.org/TakeAction
    Note:
        Model Depth 4
    Attributes:
    """

    

#TakeActionInheritedPropertiesTd = TakeActionInheritedProperties()
#TakeActionPropertiesTd = TakeActionProperties()


class AllProperties(TakeActionInheritedProperties , TakeActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[TakeActionProperties, TakeActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "TakeAction"
    return model
    

TakeAction = create_schema_org_model()