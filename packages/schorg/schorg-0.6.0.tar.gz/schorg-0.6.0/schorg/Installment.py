"""
Represents the installment pricing component of the total price for an offered product.

https://schema.org/Installment
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class InstallmentInheritedProperties(TypedDict):
    """Represents the installment pricing component of the total price for an offered product.

    References:
        https://schema.org/Installment
    Note:
        Model Depth 5
    Attributes:
    """

    


class InstallmentProperties(TypedDict):
    """Represents the installment pricing component of the total price for an offered product.

    References:
        https://schema.org/Installment
    Note:
        Model Depth 5
    Attributes:
    """

    

#InstallmentInheritedPropertiesTd = InstallmentInheritedProperties()
#InstallmentPropertiesTd = InstallmentProperties()


class AllProperties(InstallmentInheritedProperties , InstallmentProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[InstallmentProperties, InstallmentInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Installment"
    return model
    

Installment = create_schema_org_model()