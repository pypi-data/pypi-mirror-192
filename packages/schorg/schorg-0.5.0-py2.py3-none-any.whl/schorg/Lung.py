"""
Lung and respiratory system clinical examination.

https://schema.org/Lung
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class LungInheritedProperties(TypedDict):
    """Lung and respiratory system clinical examination.

    References:
        https://schema.org/Lung
    Note:
        Model Depth 5
    Attributes:
    """

    


class LungProperties(TypedDict):
    """Lung and respiratory system clinical examination.

    References:
        https://schema.org/Lung
    Note:
        Model Depth 5
    Attributes:
    """

    

#LungInheritedPropertiesTd = LungInheritedProperties()
#LungPropertiesTd = LungProperties()


class AllProperties(LungInheritedProperties , LungProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[LungProperties, LungInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Lung"
    return model
    

Lung = create_schema_org_model()