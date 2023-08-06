"""
Bank or credit union.

https://schema.org/BankOrCreditUnion
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BankOrCreditUnionInheritedProperties(TypedDict):
    """Bank or credit union.

    References:
        https://schema.org/BankOrCreditUnion
    Note:
        Model Depth 5
    Attributes:
        feesAndCommissionsSpecification: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): Description of fees, commissions, and other terms applied either to a class of financial product, or by a financial service organization.
    """

    feesAndCommissionsSpecification: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    


class BankOrCreditUnionProperties(TypedDict):
    """Bank or credit union.

    References:
        https://schema.org/BankOrCreditUnion
    Note:
        Model Depth 5
    Attributes:
    """

    

#BankOrCreditUnionInheritedPropertiesTd = BankOrCreditUnionInheritedProperties()
#BankOrCreditUnionPropertiesTd = BankOrCreditUnionProperties()


class AllProperties(BankOrCreditUnionInheritedProperties , BankOrCreditUnionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BankOrCreditUnionProperties, BankOrCreditUnionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BankOrCreditUnion"
    return model
    

BankOrCreditUnion = create_schema_org_model()