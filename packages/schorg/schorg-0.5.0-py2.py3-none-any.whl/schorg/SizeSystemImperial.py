"""
Imperial size system.

https://schema.org/SizeSystemImperial
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SizeSystemImperialInheritedProperties(TypedDict):
    """Imperial size system.

    References:
        https://schema.org/SizeSystemImperial
    Note:
        Model Depth 5
    Attributes:
    """

    


class SizeSystemImperialProperties(TypedDict):
    """Imperial size system.

    References:
        https://schema.org/SizeSystemImperial
    Note:
        Model Depth 5
    Attributes:
    """

    

#SizeSystemImperialInheritedPropertiesTd = SizeSystemImperialInheritedProperties()
#SizeSystemImperialPropertiesTd = SizeSystemImperialProperties()


class AllProperties(SizeSystemImperialInheritedProperties , SizeSystemImperialProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SizeSystemImperialProperties, SizeSystemImperialInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "SizeSystemImperial"
    return model
    

SizeSystemImperial = create_schema_org_model()