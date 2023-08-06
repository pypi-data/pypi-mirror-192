"""
Specifies that there is a finite window for product returns.

https://schema.org/MerchantReturnFiniteReturnWindow
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MerchantReturnFiniteReturnWindowInheritedProperties(TypedDict):
    """Specifies that there is a finite window for product returns.

    References:
        https://schema.org/MerchantReturnFiniteReturnWindow
    Note:
        Model Depth 5
    Attributes:
    """

    


class MerchantReturnFiniteReturnWindowProperties(TypedDict):
    """Specifies that there is a finite window for product returns.

    References:
        https://schema.org/MerchantReturnFiniteReturnWindow
    Note:
        Model Depth 5
    Attributes:
    """

    

#MerchantReturnFiniteReturnWindowInheritedPropertiesTd = MerchantReturnFiniteReturnWindowInheritedProperties()
#MerchantReturnFiniteReturnWindowPropertiesTd = MerchantReturnFiniteReturnWindowProperties()


class AllProperties(MerchantReturnFiniteReturnWindowInheritedProperties , MerchantReturnFiniteReturnWindowProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MerchantReturnFiniteReturnWindowProperties, MerchantReturnFiniteReturnWindowInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MerchantReturnFiniteReturnWindow"
    return model
    

MerchantReturnFiniteReturnWindow = create_schema_org_model()