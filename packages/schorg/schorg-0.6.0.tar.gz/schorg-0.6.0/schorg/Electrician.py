"""
An electrician.

https://schema.org/Electrician
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ElectricianInheritedProperties(TypedDict):
    """An electrician.

    References:
        https://schema.org/Electrician
    Note:
        Model Depth 5
    Attributes:
    """

    


class ElectricianProperties(TypedDict):
    """An electrician.

    References:
        https://schema.org/Electrician
    Note:
        Model Depth 5
    Attributes:
    """

    

#ElectricianInheritedPropertiesTd = ElectricianInheritedProperties()
#ElectricianPropertiesTd = ElectricianProperties()


class AllProperties(ElectricianInheritedProperties , ElectricianProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ElectricianProperties, ElectricianInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Electrician"
    return model
    

Electrician = create_schema_org_model()