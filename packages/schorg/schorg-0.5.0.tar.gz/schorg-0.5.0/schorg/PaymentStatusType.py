"""
A specific payment status. For example, PaymentDue, PaymentComplete, etc.

https://schema.org/PaymentStatusType
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PaymentStatusTypeInheritedProperties(TypedDict):
    """A specific payment status. For example, PaymentDue, PaymentComplete, etc.

    References:
        https://schema.org/PaymentStatusType
    Note:
        Model Depth 5
    Attributes:
    """

    


class PaymentStatusTypeProperties(TypedDict):
    """A specific payment status. For example, PaymentDue, PaymentComplete, etc.

    References:
        https://schema.org/PaymentStatusType
    Note:
        Model Depth 5
    Attributes:
    """

    

#PaymentStatusTypeInheritedPropertiesTd = PaymentStatusTypeInheritedProperties()
#PaymentStatusTypePropertiesTd = PaymentStatusTypeProperties()


class AllProperties(PaymentStatusTypeInheritedProperties , PaymentStatusTypeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PaymentStatusTypeProperties, PaymentStatusTypeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PaymentStatusType"
    return model
    

PaymentStatusType = create_schema_org_model()