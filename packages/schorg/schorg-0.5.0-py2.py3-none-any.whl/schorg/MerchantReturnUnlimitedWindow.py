"""
Specifies that there is an unlimited window for product returns.

https://schema.org/MerchantReturnUnlimitedWindow
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MerchantReturnUnlimitedWindowInheritedProperties(TypedDict):
    """Specifies that there is an unlimited window for product returns.

    References:
        https://schema.org/MerchantReturnUnlimitedWindow
    Note:
        Model Depth 5
    Attributes:
    """

    


class MerchantReturnUnlimitedWindowProperties(TypedDict):
    """Specifies that there is an unlimited window for product returns.

    References:
        https://schema.org/MerchantReturnUnlimitedWindow
    Note:
        Model Depth 5
    Attributes:
    """

    

#MerchantReturnUnlimitedWindowInheritedPropertiesTd = MerchantReturnUnlimitedWindowInheritedProperties()
#MerchantReturnUnlimitedWindowPropertiesTd = MerchantReturnUnlimitedWindowProperties()


class AllProperties(MerchantReturnUnlimitedWindowInheritedProperties , MerchantReturnUnlimitedWindowProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MerchantReturnUnlimitedWindowProperties, MerchantReturnUnlimitedWindowInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MerchantReturnUnlimitedWindow"
    return model
    

MerchantReturnUnlimitedWindow = create_schema_org_model()