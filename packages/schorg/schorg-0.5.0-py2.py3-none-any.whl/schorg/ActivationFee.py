"""
Represents the activation fee part of the total price for an offered product, for example a cellphone contract.

https://schema.org/ActivationFee
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ActivationFeeInheritedProperties(TypedDict):
    """Represents the activation fee part of the total price for an offered product, for example a cellphone contract.

    References:
        https://schema.org/ActivationFee
    Note:
        Model Depth 5
    Attributes:
    """

    


class ActivationFeeProperties(TypedDict):
    """Represents the activation fee part of the total price for an offered product, for example a cellphone contract.

    References:
        https://schema.org/ActivationFee
    Note:
        Model Depth 5
    Attributes:
    """

    

#ActivationFeeInheritedPropertiesTd = ActivationFeeInheritedProperties()
#ActivationFeePropertiesTd = ActivationFeeProperties()


class AllProperties(ActivationFeeInheritedProperties , ActivationFeeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ActivationFeeProperties, ActivationFeeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ActivationFee"
    return model
    

ActivationFee = create_schema_org_model()