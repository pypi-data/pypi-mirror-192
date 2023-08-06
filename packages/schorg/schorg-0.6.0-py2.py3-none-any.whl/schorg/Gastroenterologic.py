"""
A specific branch of medical science that pertains to diagnosis and treatment of disorders of digestive system.

https://schema.org/Gastroenterologic
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class GastroenterologicInheritedProperties(TypedDict):
    """A specific branch of medical science that pertains to diagnosis and treatment of disorders of digestive system.

    References:
        https://schema.org/Gastroenterologic
    Note:
        Model Depth 6
    Attributes:
    """

    


class GastroenterologicProperties(TypedDict):
    """A specific branch of medical science that pertains to diagnosis and treatment of disorders of digestive system.

    References:
        https://schema.org/Gastroenterologic
    Note:
        Model Depth 6
    Attributes:
    """

    

#GastroenterologicInheritedPropertiesTd = GastroenterologicInheritedProperties()
#GastroenterologicPropertiesTd = GastroenterologicProperties()


class AllProperties(GastroenterologicInheritedProperties , GastroenterologicProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[GastroenterologicProperties, GastroenterologicInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Gastroenterologic"
    return model
    

Gastroenterologic = create_schema_org_model()