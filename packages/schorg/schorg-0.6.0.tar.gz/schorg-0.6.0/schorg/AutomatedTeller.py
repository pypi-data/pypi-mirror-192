"""
ATM/cash machine.

https://schema.org/AutomatedTeller
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AutomatedTellerInheritedProperties(TypedDict):
    """ATM/cash machine.

    References:
        https://schema.org/AutomatedTeller
    Note:
        Model Depth 5
    Attributes:
        feesAndCommissionsSpecification: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): Description of fees, commissions, and other terms applied either to a class of financial product, or by a financial service organization.
    """

    feesAndCommissionsSpecification: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    


class AutomatedTellerProperties(TypedDict):
    """ATM/cash machine.

    References:
        https://schema.org/AutomatedTeller
    Note:
        Model Depth 5
    Attributes:
    """

    

#AutomatedTellerInheritedPropertiesTd = AutomatedTellerInheritedProperties()
#AutomatedTellerPropertiesTd = AutomatedTellerProperties()


class AllProperties(AutomatedTellerInheritedProperties , AutomatedTellerProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AutomatedTellerProperties, AutomatedTellerInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "AutomatedTeller"
    return model
    

AutomatedTeller = create_schema_org_model()