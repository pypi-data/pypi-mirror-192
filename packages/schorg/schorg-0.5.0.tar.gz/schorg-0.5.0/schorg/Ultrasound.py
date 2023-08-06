"""
Ultrasound imaging.

https://schema.org/Ultrasound
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class UltrasoundInheritedProperties(TypedDict):
    """Ultrasound imaging.

    References:
        https://schema.org/Ultrasound
    Note:
        Model Depth 6
    Attributes:
    """

    


class UltrasoundProperties(TypedDict):
    """Ultrasound imaging.

    References:
        https://schema.org/Ultrasound
    Note:
        Model Depth 6
    Attributes:
    """

    

#UltrasoundInheritedPropertiesTd = UltrasoundInheritedProperties()
#UltrasoundPropertiesTd = UltrasoundProperties()


class AllProperties(UltrasoundInheritedProperties , UltrasoundProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[UltrasoundProperties, UltrasoundInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Ultrasound"
    return model
    

Ultrasound = create_schema_org_model()