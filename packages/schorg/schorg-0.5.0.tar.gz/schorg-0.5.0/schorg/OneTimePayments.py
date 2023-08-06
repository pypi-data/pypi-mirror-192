"""
OneTimePayments: this is a benefit for one-time payments for individuals.

https://schema.org/OneTimePayments
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OneTimePaymentsInheritedProperties(TypedDict):
    """OneTimePayments: this is a benefit for one-time payments for individuals.

    References:
        https://schema.org/OneTimePayments
    Note:
        Model Depth 5
    Attributes:
    """

    


class OneTimePaymentsProperties(TypedDict):
    """OneTimePayments: this is a benefit for one-time payments for individuals.

    References:
        https://schema.org/OneTimePayments
    Note:
        Model Depth 5
    Attributes:
    """

    

#OneTimePaymentsInheritedPropertiesTd = OneTimePaymentsInheritedProperties()
#OneTimePaymentsPropertiesTd = OneTimePaymentsProperties()


class AllProperties(OneTimePaymentsInheritedProperties , OneTimePaymentsProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OneTimePaymentsProperties, OneTimePaymentsInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OneTimePayments"
    return model
    

OneTimePayments = create_schema_org_model()