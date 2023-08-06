"""
Accountancy business.As a [[LocalBusiness]] it can be described as a [[provider]] of one or more [[Service]]\(s).      

https://schema.org/AccountingService
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AccountingServiceInheritedProperties(TypedDict):
    """Accountancy business.As a [[LocalBusiness]] it can be described as a [[provider]] of one or more [[Service]]\(s).      

    References:
        https://schema.org/AccountingService
    Note:
        Model Depth 5
    Attributes:
        feesAndCommissionsSpecification: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): Description of fees, commissions, and other terms applied either to a class of financial product, or by a financial service organization.
    """

    feesAndCommissionsSpecification: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    


class AccountingServiceProperties(TypedDict):
    """Accountancy business.As a [[LocalBusiness]] it can be described as a [[provider]] of one or more [[Service]]\(s).      

    References:
        https://schema.org/AccountingService
    Note:
        Model Depth 5
    Attributes:
    """

    

#AccountingServiceInheritedPropertiesTd = AccountingServiceInheritedProperties()
#AccountingServicePropertiesTd = AccountingServiceProperties()


class AllProperties(AccountingServiceInheritedProperties , AccountingServiceProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AccountingServiceProperties, AccountingServiceInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "AccountingService"
    return model
    

AccountingService = create_schema_org_model()