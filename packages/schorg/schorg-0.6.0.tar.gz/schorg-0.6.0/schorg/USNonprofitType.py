"""
USNonprofitType: Non-profit organization type originating from the United States.

https://schema.org/USNonprofitType
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class USNonprofitTypeInheritedProperties(TypedDict):
    """USNonprofitType: Non-profit organization type originating from the United States.

    References:
        https://schema.org/USNonprofitType
    Note:
        Model Depth 5
    Attributes:
    """

    


class USNonprofitTypeProperties(TypedDict):
    """USNonprofitType: Non-profit organization type originating from the United States.

    References:
        https://schema.org/USNonprofitType
    Note:
        Model Depth 5
    Attributes:
    """

    

#USNonprofitTypeInheritedPropertiesTd = USNonprofitTypeInheritedProperties()
#USNonprofitTypePropertiesTd = USNonprofitTypeProperties()


class AllProperties(USNonprofitTypeInheritedProperties , USNonprofitTypeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[USNonprofitTypeProperties, USNonprofitTypeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "USNonprofitType"
    return model
    

USNonprofitType = create_schema_org_model()