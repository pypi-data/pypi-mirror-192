"""
A store that sells reading glasses and similar devices for improving vision.

https://schema.org/Optician
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OpticianInheritedProperties(TypedDict):
    """A store that sells reading glasses and similar devices for improving vision.

    References:
        https://schema.org/Optician
    Note:
        Model Depth 5
    Attributes:
    """

    


class OpticianProperties(TypedDict):
    """A store that sells reading glasses and similar devices for improving vision.

    References:
        https://schema.org/Optician
    Note:
        Model Depth 5
    Attributes:
    """

    

#OpticianInheritedPropertiesTd = OpticianInheritedProperties()
#OpticianPropertiesTd = OpticianProperties()


class AllProperties(OpticianInheritedProperties , OpticianProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OpticianProperties, OpticianInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Optician"
    return model
    

Optician = create_schema_org_model()