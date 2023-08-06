"""
Specifies that a product return policy is not provided.

https://schema.org/MerchantReturnUnspecified
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MerchantReturnUnspecifiedInheritedProperties(TypedDict):
    """Specifies that a product return policy is not provided.

    References:
        https://schema.org/MerchantReturnUnspecified
    Note:
        Model Depth 5
    Attributes:
    """

    


class MerchantReturnUnspecifiedProperties(TypedDict):
    """Specifies that a product return policy is not provided.

    References:
        https://schema.org/MerchantReturnUnspecified
    Note:
        Model Depth 5
    Attributes:
    """

    

#MerchantReturnUnspecifiedInheritedPropertiesTd = MerchantReturnUnspecifiedInheritedProperties()
#MerchantReturnUnspecifiedPropertiesTd = MerchantReturnUnspecifiedProperties()


class AllProperties(MerchantReturnUnspecifiedInheritedProperties , MerchantReturnUnspecifiedProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MerchantReturnUnspecifiedProperties, MerchantReturnUnspecifiedInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MerchantReturnUnspecified"
    return model
    

MerchantReturnUnspecified = create_schema_org_model()