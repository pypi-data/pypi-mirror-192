"""
A business that provides Heating, Ventilation and Air Conditioning services.

https://schema.org/HVACBusiness
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class HVACBusinessInheritedProperties(TypedDict):
    """A business that provides Heating, Ventilation and Air Conditioning services.

    References:
        https://schema.org/HVACBusiness
    Note:
        Model Depth 5
    Attributes:
    """

    


class HVACBusinessProperties(TypedDict):
    """A business that provides Heating, Ventilation and Air Conditioning services.

    References:
        https://schema.org/HVACBusiness
    Note:
        Model Depth 5
    Attributes:
    """

    

#HVACBusinessInheritedPropertiesTd = HVACBusinessInheritedProperties()
#HVACBusinessPropertiesTd = HVACBusinessProperties()


class AllProperties(HVACBusinessInheritedProperties , HVACBusinessProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[HVACBusinessProperties, HVACBusinessInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "HVACBusiness"
    return model
    

HVACBusiness = create_schema_org_model()