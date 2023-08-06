"""
A specific branch of medical science that pertains to diagnosis and treatment of disorders of skin.

https://schema.org/Dermatology
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DermatologyInheritedProperties(TypedDict):
    """A specific branch of medical science that pertains to diagnosis and treatment of disorders of skin.

    References:
        https://schema.org/Dermatology
    Note:
        Model Depth 5
    Attributes:
    """

    


class DermatologyProperties(TypedDict):
    """A specific branch of medical science that pertains to diagnosis and treatment of disorders of skin.

    References:
        https://schema.org/Dermatology
    Note:
        Model Depth 5
    Attributes:
    """

    

#DermatologyInheritedPropertiesTd = DermatologyInheritedProperties()
#DermatologyPropertiesTd = DermatologyProperties()


class AllProperties(DermatologyInheritedProperties , DermatologyProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DermatologyProperties, DermatologyInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Dermatology"
    return model
    

Dermatology = create_schema_org_model()