"""
A type of Bank Account with a main purpose of depositing funds to gain interest or other benefits.

https://schema.org/DepositAccount
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DepositAccountInheritedProperties(TypedDict):
    """A type of Bank Account with a main purpose of depositing funds to gain interest or other benefits.

    References:
        https://schema.org/DepositAccount
    Note:
        Model Depth 6
    Attributes:
        accountMinimumInflow: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A minimum amount that has to be paid in every month.
        accountOverdraftLimit: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): An overdraft is an extension of credit from a lending institution when an account reaches zero. An overdraft allows the individual to continue withdrawing money even if the account has no funds in it. Basically the bank allows people to borrow a set amount of money.
        bankAccountType: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): The type of a bank account.
        amount: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The amount of money.
    """

    accountMinimumInflow: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    accountOverdraftLimit: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    bankAccountType: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    amount: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    


class DepositAccountProperties(TypedDict):
    """A type of Bank Account with a main purpose of depositing funds to gain interest or other benefits.

    References:
        https://schema.org/DepositAccount
    Note:
        Model Depth 6
    Attributes:
    """

    

#DepositAccountInheritedPropertiesTd = DepositAccountInheritedProperties()
#DepositAccountPropertiesTd = DepositAccountProperties()


class AllProperties(DepositAccountInheritedProperties , DepositAccountProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DepositAccountProperties, DepositAccountInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DepositAccount"
    return model
    

DepositAccount = create_schema_org_model()