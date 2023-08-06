"""
Specifies that product returns are not permitted.

https://schema.org/MerchantReturnNotPermitted
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MerchantReturnNotPermittedInheritedProperties(TypedDict):
    """Specifies that product returns are not permitted.

    References:
        https://schema.org/MerchantReturnNotPermitted
    Note:
        Model Depth 5
    Attributes:
    """

    


class MerchantReturnNotPermittedProperties(TypedDict):
    """Specifies that product returns are not permitted.

    References:
        https://schema.org/MerchantReturnNotPermitted
    Note:
        Model Depth 5
    Attributes:
    """

    

#MerchantReturnNotPermittedInheritedPropertiesTd = MerchantReturnNotPermittedInheritedProperties()
#MerchantReturnNotPermittedPropertiesTd = MerchantReturnNotPermittedProperties()


class AllProperties(MerchantReturnNotPermittedInheritedProperties , MerchantReturnNotPermittedProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MerchantReturnNotPermittedProperties, MerchantReturnNotPermittedInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MerchantReturnNotPermitted"
    return model
    

MerchantReturnNotPermitted = create_schema_org_model()