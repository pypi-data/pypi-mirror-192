"""
The act of physically/electronically dispatching an object for transfer from an origin to a destination. Related actions:* [[ReceiveAction]]: The reciprocal of SendAction.* [[GiveAction]]: Unlike GiveAction, SendAction does not imply the transfer of ownership (e.g. I can send you my laptop, but I'm not necessarily giving it to you).

https://schema.org/SendAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SendActionInheritedProperties(TypedDict):
    """The act of physically/electronically dispatching an object for transfer from an origin to a destination. Related actions:* [[ReceiveAction]]: The reciprocal of SendAction.* [[GiveAction]]: Unlike GiveAction, SendAction does not imply the transfer of ownership (e.g. I can send you my laptop, but I'm not necessarily giving it to you).

    References:
        https://schema.org/SendAction
    Note:
        Model Depth 4
    Attributes:
        toLocation: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of location. The final location of the object or the agent after the action.
        fromLocation: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of location. The original location of the object or the agent before the action.
    """

    toLocation: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    fromLocation: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class SendActionProperties(TypedDict):
    """The act of physically/electronically dispatching an object for transfer from an origin to a destination. Related actions:* [[ReceiveAction]]: The reciprocal of SendAction.* [[GiveAction]]: Unlike GiveAction, SendAction does not imply the transfer of ownership (e.g. I can send you my laptop, but I'm not necessarily giving it to you).

    References:
        https://schema.org/SendAction
    Note:
        Model Depth 4
    Attributes:
        deliveryMethod: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of instrument. The method of delivery.
        recipient: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of participant. The participant who is at the receiving end of the action.
    """

    deliveryMethod: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    recipient: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#SendActionInheritedPropertiesTd = SendActionInheritedProperties()
#SendActionPropertiesTd = SendActionProperties()


class AllProperties(SendActionInheritedProperties , SendActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SendActionProperties, SendActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "SendAction"
    return model
    

SendAction = create_schema_org_model()