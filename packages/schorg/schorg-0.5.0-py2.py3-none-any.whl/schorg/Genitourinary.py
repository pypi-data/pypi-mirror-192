"""
Genitourinary system function assessment with clinical examination.

https://schema.org/Genitourinary
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class GenitourinaryInheritedProperties(TypedDict):
    """Genitourinary system function assessment with clinical examination.

    References:
        https://schema.org/Genitourinary
    Note:
        Model Depth 5
    Attributes:
    """

    


class GenitourinaryProperties(TypedDict):
    """Genitourinary system function assessment with clinical examination.

    References:
        https://schema.org/Genitourinary
    Note:
        Model Depth 5
    Attributes:
    """

    

#GenitourinaryInheritedPropertiesTd = GenitourinaryInheritedProperties()
#GenitourinaryPropertiesTd = GenitourinaryProperties()


class AllProperties(GenitourinaryInheritedProperties , GenitourinaryProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[GenitourinaryProperties, GenitourinaryInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Genitourinary"
    return model
    

Genitourinary = create_schema_org_model()