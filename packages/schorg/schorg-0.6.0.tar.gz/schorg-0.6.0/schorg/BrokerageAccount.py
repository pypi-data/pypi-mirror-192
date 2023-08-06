"""
An account that allows an investor to deposit funds and place investment orders with a licensed broker or brokerage firm.

https://schema.org/BrokerageAccount
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BrokerageAccountInheritedProperties(TypedDict):
    """An account that allows an investor to deposit funds and place investment orders with a licensed broker or brokerage firm.

    References:
        https://schema.org/BrokerageAccount
    Note:
        Model Depth 6
    Attributes:
        amount: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The amount of money.
    """

    amount: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    


class BrokerageAccountProperties(TypedDict):
    """An account that allows an investor to deposit funds and place investment orders with a licensed broker or brokerage firm.

    References:
        https://schema.org/BrokerageAccount
    Note:
        Model Depth 6
    Attributes:
    """

    

#BrokerageAccountInheritedPropertiesTd = BrokerageAccountInheritedProperties()
#BrokerageAccountPropertiesTd = BrokerageAccountProperties()


class AllProperties(BrokerageAccountInheritedProperties , BrokerageAccountProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BrokerageAccountProperties, BrokerageAccountInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BrokerageAccount"
    return model
    

BrokerageAccount = create_schema_org_model()