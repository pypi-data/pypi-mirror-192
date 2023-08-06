"""
The act of transferring money from one place to another place. This may occur electronically or physically.

https://schema.org/MoneyTransfer
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MoneyTransferInheritedProperties(TypedDict):
    """The act of transferring money from one place to another place. This may occur electronically or physically.

    References:
        https://schema.org/MoneyTransfer
    Note:
        Model Depth 4
    Attributes:
        toLocation: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of location. The final location of the object or the agent after the action.
        fromLocation: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of location. The original location of the object or the agent before the action.
    """

    toLocation: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    fromLocation: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class MoneyTransferProperties(TypedDict):
    """The act of transferring money from one place to another place. This may occur electronically or physically.

    References:
        https://schema.org/MoneyTransfer
    Note:
        Model Depth 4
    Attributes:
        amount: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The amount of money.
        beneficiaryBank: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A bank or bank’s branch, financial institution or international financial institution operating the beneficiary’s bank account or releasing funds for the beneficiary.
    """

    amount: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    beneficiaryBank: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    

#MoneyTransferInheritedPropertiesTd = MoneyTransferInheritedProperties()
#MoneyTransferPropertiesTd = MoneyTransferProperties()


class AllProperties(MoneyTransferInheritedProperties , MoneyTransferProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MoneyTransferProperties, MoneyTransferInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MoneyTransfer"
    return model
    

MoneyTransfer = create_schema_org_model()