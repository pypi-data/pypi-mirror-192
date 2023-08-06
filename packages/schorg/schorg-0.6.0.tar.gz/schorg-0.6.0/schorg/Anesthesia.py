"""
A specific branch of medical science that pertains to study of anesthetics and their application.

https://schema.org/Anesthesia
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AnesthesiaInheritedProperties(TypedDict):
    """A specific branch of medical science that pertains to study of anesthetics and their application.

    References:
        https://schema.org/Anesthesia
    Note:
        Model Depth 6
    Attributes:
    """

    


class AnesthesiaProperties(TypedDict):
    """A specific branch of medical science that pertains to study of anesthetics and their application.

    References:
        https://schema.org/Anesthesia
    Note:
        Model Depth 6
    Attributes:
    """

    

#AnesthesiaInheritedPropertiesTd = AnesthesiaInheritedProperties()
#AnesthesiaPropertiesTd = AnesthesiaProperties()


class AllProperties(AnesthesiaInheritedProperties , AnesthesiaProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AnesthesiaProperties, AnesthesiaInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Anesthesia"
    return model
    

Anesthesia = create_schema_org_model()