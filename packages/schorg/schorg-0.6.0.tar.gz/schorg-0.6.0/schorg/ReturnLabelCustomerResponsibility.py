"""
Indicated that creating a return label is the responsibility of the customer.

https://schema.org/ReturnLabelCustomerResponsibility
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ReturnLabelCustomerResponsibilityInheritedProperties(TypedDict):
    """Indicated that creating a return label is the responsibility of the customer.

    References:
        https://schema.org/ReturnLabelCustomerResponsibility
    Note:
        Model Depth 5
    Attributes:
    """

    


class ReturnLabelCustomerResponsibilityProperties(TypedDict):
    """Indicated that creating a return label is the responsibility of the customer.

    References:
        https://schema.org/ReturnLabelCustomerResponsibility
    Note:
        Model Depth 5
    Attributes:
    """

    

#ReturnLabelCustomerResponsibilityInheritedPropertiesTd = ReturnLabelCustomerResponsibilityInheritedProperties()
#ReturnLabelCustomerResponsibilityPropertiesTd = ReturnLabelCustomerResponsibilityProperties()


class AllProperties(ReturnLabelCustomerResponsibilityInheritedProperties , ReturnLabelCustomerResponsibilityProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ReturnLabelCustomerResponsibilityProperties, ReturnLabelCustomerResponsibilityInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ReturnLabelCustomerResponsibility"
    return model
    

ReturnLabelCustomerResponsibility = create_schema_org_model()