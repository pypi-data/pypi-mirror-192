"""
UKNonprofitType: Non-profit organization type originating from the United Kingdom.

https://schema.org/UKNonprofitType
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class UKNonprofitTypeInheritedProperties(TypedDict):
    """UKNonprofitType: Non-profit organization type originating from the United Kingdom.

    References:
        https://schema.org/UKNonprofitType
    Note:
        Model Depth 5
    Attributes:
    """

    


class UKNonprofitTypeProperties(TypedDict):
    """UKNonprofitType: Non-profit organization type originating from the United Kingdom.

    References:
        https://schema.org/UKNonprofitType
    Note:
        Model Depth 5
    Attributes:
    """

    

#UKNonprofitTypeInheritedPropertiesTd = UKNonprofitTypeInheritedProperties()
#UKNonprofitTypePropertiesTd = UKNonprofitTypeProperties()


class AllProperties(UKNonprofitTypeInheritedProperties , UKNonprofitTypeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[UKNonprofitTypeProperties, UKNonprofitTypeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "UKNonprofitType"
    return model
    

UKNonprofitType = create_schema_org_model()