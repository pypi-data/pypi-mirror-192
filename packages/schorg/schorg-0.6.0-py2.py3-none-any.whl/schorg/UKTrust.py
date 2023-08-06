"""
UKTrust: Non-profit type referring to a UK trust.

https://schema.org/UKTrust
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class UKTrustInheritedProperties(TypedDict):
    """UKTrust: Non-profit type referring to a UK trust.

    References:
        https://schema.org/UKTrust
    Note:
        Model Depth 6
    Attributes:
    """

    


class UKTrustProperties(TypedDict):
    """UKTrust: Non-profit type referring to a UK trust.

    References:
        https://schema.org/UKTrust
    Note:
        Model Depth 6
    Attributes:
    """

    

#UKTrustInheritedPropertiesTd = UKTrustInheritedProperties()
#UKTrustPropertiesTd = UKTrustProperties()


class AllProperties(UKTrustInheritedProperties , UKTrustProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[UKTrustProperties, UKTrustInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "UKTrust"
    return model
    

UKTrust = create_schema_org_model()