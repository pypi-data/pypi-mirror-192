"""
Pathogenic bacteria that cause bacterial infection.

https://schema.org/Bacteria
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BacteriaInheritedProperties(TypedDict):
    """Pathogenic bacteria that cause bacterial infection.

    References:
        https://schema.org/Bacteria
    Note:
        Model Depth 6
    Attributes:
    """

    


class BacteriaProperties(TypedDict):
    """Pathogenic bacteria that cause bacterial infection.

    References:
        https://schema.org/Bacteria
    Note:
        Model Depth 6
    Attributes:
    """

    

#BacteriaInheritedPropertiesTd = BacteriaInheritedProperties()
#BacteriaPropertiesTd = BacteriaProperties()


class AllProperties(BacteriaInheritedProperties , BacteriaProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BacteriaProperties, BacteriaInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Bacteria"
    return model
    

Bacteria = create_schema_org_model()